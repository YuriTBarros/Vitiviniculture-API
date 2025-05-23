import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import os


class ProcessingScraper:
    def __init__(self):
        self.years = None

    def sync(self, base_url, file_path, file_name):
        """
        Attempts to fetch and clean importation data from Embrapa.
        Falls back to loading local CSV if scraping fails.

        Returns:
            list[dict]: JSON-serializable data.
        """
        try:
            self._get_year(base_url)
            df = self._processing_table(base_url)
            if df.empty:
                return False

            # Apply a series of cleaning and transformation functions
            df = self._encode_latin1(df)
            df = self._clean_quantities(df)
            df = self._categorize(df)
            df = self._remove_categories(df)
            df = self._remove_nan(df)
            df = self._remove_total(df)
            df = self._suboptions_labeling(df)

            self._save_df(df, file_path, file_name)
            return True

        except Exception as e:
            print(f"[WARN] Scraper failed. Reason: {e}")
            return False

    def _get_year(self, base_url):
        try:
            response = requests.get(base_url + "?opcao=opt_03")
            response.raise_for_status()
        except RequestException as e:
            print(f"[ERROR] Failed to connect to Embrapa: {e}")
            raise

        soup = BeautifulSoup(response.content, "html.parser")
        select_years = soup.find("input", {"class": "text_pesq"})
        self.years = [
            year
            for year in range(
                int(select_years["min"]), int(select_years["max"]) + 1
            )
        ]

    def _categorize(self, df: pd.DataFrame):
        current_category = None
        categories = []

        for product in df["Cultivar"]:
            product_str = str(product).strip()

            if product_str.isupper() and product_str != "NAN":
                current_category = product_str

            categories.append(current_category)

        df["Categoria"] = categories
        return df

    def _remove_categories(self, df):
        mask = df["Cultivar"].apply(
            lambda x: isinstance(x, str) and not x.strip().isupper()
        )
        return df[mask].reset_index(drop=True)

    def _processing_table(self, base_url):
        dfs = []
        for year in self.years:
            for subop in range(1, 5):  # subopt_01 to subopt_04
                suboption = f"subopt_0{subop}"
                url = (
                    f"{base_url}?subopcao={suboption}"
                    f"&opcao=opt_03"
                    f"&ano={year}"
                )
                try:
                    print(f"Requesting {url}...")
                    df_year = pd.read_html(url)[3]
                    df_year["ano"] = year
                    df_year["subopcao"] = suboption
                    dfs.append(df_year)
                except Exception as e:
                    print(f"Error in {year}, suboption {suboption}: {e}")
                    raise
        if not dfs:
            return pd.DataFrame()
        df_final = pd.concat(dfs, ignore_index=True)

        # Remove  columns 'Unnamed: 2' and / or 'Sem definiÃ§Ã£o' if required
        if "Unnamed: 2" or "Sem definiÃ§Ã£o" in df_final.columns:
            columns_to_remove = ["Unnamed: 2", "Sem definiÃ§Ã£o"]
            df_final = df_final.drop(
                columns=[
                    col for col in columns_to_remove if col in df_final.columns
                ]
            )

        # Calls the function Categorize
        df_final = self.categorize(df_final)

        return df_final

    def _encode_latin1(self, df: pd.DataFrame) -> pd.DataFrame:
        def try_fix_encoding(x):
            if not isinstance(x, str):
                return x
            try:
                # change from latin1 to utf-8 if required
                return x.encode("latin1").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                return x  # If fails, original is returned

        if "Cultivar" in df.columns:
            df["Cultivar"] = df["Cultivar"].astype(str).apply(try_fix_encoding)
        return df

    def _clean_quantities(self, df):
        if "Quantidade (Kg)" in df.columns:
            df["Quantidade (Kg)"] = df["Quantidade (Kg)"].replace("-", "0")
            df["Quantidade (Kg)"] = (
                df["Quantidade (Kg)"]
                .astype(str)
                .str.replace(".", "", regex=False)
                .str.replace("-", "", regex=False)
                .str.strip()
            )
            df["Quantidade (Kg)"] = pd.to_numeric(
                df["Quantidade (Kg)"], errors="coerce"
            )
        return df

    def _remove_nan(self, df):
        df = df.dropna(axis=0)
        return df

    def _remove_total(self, df):
        df = df[df["Cultivar"] != "Total"]
        return df

    def _suboptions_labeling(self, df):
        map = {
            "subopt_01": "Viníferas",
            "subopt_02": "Americanas e híbridas",
            "subopt_03": "Uvas de mesa",
            "subopt_04": "Sem classificação",
        }
        df["subopcao"] = df["subopcao"].map(map)
        return df

    def _save_df(self, df, file_path, file_name):
        """
        Saves the cleaned DataFrame as both CSV and JSON files.

        Args:
            df (pd.DataFrame): The DataFrame to be saved.
            file_path (str): The path where the files will be saved.
            file_name (str): The base name of the files to be saved.
        """
        os.makedirs(file_path, exist_ok=True)

        filepath = os.path.join(file_path, f"{file_name}.csv")
        df.to_csv(filepath, index=False)

        filepath_json = os.path.join(file_path, f"{file_name}.json")
        df.to_json(filepath_json, orient="records", force_ascii=False)
