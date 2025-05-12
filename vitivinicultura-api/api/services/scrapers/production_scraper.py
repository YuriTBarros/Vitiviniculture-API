import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import os


class ProductionScraper:
    def __init__(self):
        self.years = None

    def sync(self, base_url, file_path, file_name):
        """
        Main function that coordinates the scraping of data, cleans it,
            and saves the results.

        Args:
            base_url (str): The base URL for scraping the data.
            file_path (str): The path where the files will be saved.
            file_name (str): The name of the file to be saved.

        Returns:
            bool: Returns True if scraping and cleaning were successful,
                False otherwise.
        """
        try:
            self._get_year(base_url)
            df = self._production_table(base_url)
            if df.empty:
                return False

            df = self._encode_latin1(df)
            df = self._clean_quantities(df)
            df = self._categorize(df)
            df = self._remove_categories(df)
            df = self._remove_nan(df)
            df = self._remove_total(df)

            self._save_df(df, file_path, file_name)
            return True

        except Exception as e:
            print(f"[WARN] Scraper failed. Reason: {e}")
            return False

    def _get_year(self, base_url):
        try:
            response = requests.get(base_url + "?opcao=opt_02")
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

        for product in df["Produto"]:
            product_str = str(product).strip()

            if product_str.isupper() and product_str != "NAN":
                current_category = product_str

            categories.append(current_category)

        df["Categoria"] = categories
        return df

    def _remove_categories(self, df):
        if "Produto" not in df.columns:
            return df
        mask = df["Produto"].apply(
            lambda x: isinstance(x, str) and not x.strip().isupper()
        )
        return df[mask].reset_index(drop=True)

    def _production_table(self, base_url):
        dfs = []
        for year in self.years:
            url = f"{base_url}?ano={year}&opcao=opt_02"
            try:
                print(f"Requesting {url}...")
                df_year = pd.read_html(url)[3]
                df_year["ano"] = year
                dfs.append(df_year)
            except Exception as e:
                print(f"Erro in {year}: {e}")
                raise
        if not dfs:
            return pd.DataFrame()
        df_final = pd.concat(dfs, ignore_index=True)

        #  Remove column 'Unnamed: 2' if necessary.
        if "Unnamed: 2" in df_final.columns:
            df_final = df_final.drop(columns="Unnamed: 2")

        # Calls the function Categorize
        df_final = self._categorize(df_final)

        return df_final

    def _encode_latin1(self, df):
        def try_fix_encoding(x):
            if not isinstance(x, str):
                return x
            try:
                return x.encode("latin1").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                return x

        if "Produto" in df.columns:
            df["Produto"] = df["Produto"].astype(str).apply(try_fix_encoding)
        return df

    def _clean_quantities(self, df):
        if "Quantidade (L.)" in df.columns:
            df["Quantidade (L.)"] = df["Quantidade (L.)"].replace("-", "0")
            df["Quantidade (L.)"] = (
                df["Quantidade (L.)"]
                .astype(str)
                .str.replace(".", "", regex=False)
                .str.replace("-", "", regex=False)
                .str.strip()
            )
            df["Quantidade (L.)"] = pd.to_numeric(
                df["Quantidade (L.)"], errors="coerce"
            )
        return df

    def _remove_nan(self, df):
        df = df.dropna(axis=0)
        return df

    def _remove_total(self, df):
        df = df[df["Produto"] != "Total"]
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
