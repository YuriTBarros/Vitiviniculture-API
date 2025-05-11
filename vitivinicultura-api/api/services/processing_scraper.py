import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import os


class ProcessingScraper:
    def __init__(self):
        self.base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
        self.years = None

    def get_year(self):
        try:
            response = requests.get(self.base_url + "?opcao=opt_03")
            response.raise_for_status()
        except RequestException as e:
            print(f"[ERROR] Failed to connect to Embrapa: {e}")
            self.years = []
            return

        soup = BeautifulSoup(response.content, "html.parser")
        select_years = soup.find("input", {"class": "text_pesq"})
        self.years = [
            year
            for year in range(
                int(select_years["min"]), int(select_years["max"]) + 1
            )
        ]

    def categorize(self, df: pd.DataFrame):
        current_category = None
        categories = []

        for product in df["Cultivar"]:
            product_str = str(product).strip()

            if product_str.isupper() and product_str != "NAN":
                current_category = product_str

            categories.append(current_category)

        df["Categoria"] = categories
        return df

    def remove_categories(self, df):
        mask = df["Cultivar"].apply(
            lambda x: isinstance(x, str) and not x.strip().isupper()
        )
        return df[mask].reset_index(drop=True)

    def processing_table(self):
        dfs = []
        for year in self.years:
            for subop in range(1, 5):  # subopt_01 to subopt_04
                suboption = f"subopt_0{subop}"
                url = (
                    f"{self.base_url}?subopcao={suboption}"
                    f"&opcao=opt_03"
                    f"&ano={year}"
                )
                try:
                    df_year = pd.read_html(url)[3]
                    df_year["ano"] = year
                    df_year["subopcao"] = suboption
                    dfs.append(df_year)
                except Exception as e:
                    print(f"Error in {year}, suboption {suboption}: {e}")
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

    def encode_latin1(self, df: pd.DataFrame) -> pd.DataFrame:
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

    def clean_quantities(self, df):
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

    def remove_nan(self, df):
        df = df.dropna(axis=0)
        return df

    def remove_total(self, df):
        df = df[df["Cultivar"] != "Total"]
        return df

    def suboptions_labeling(self, df):
        map = {
            "subopt_01": "Viníferas",
            "subopt_02": "Americanas e híbridas",
            "subopt_03": "Uvas de mesa",
            "subopt_04": "Sem classificação",
        }
        df["subopcao"] = df["subopcao"].map(map)
        return df

    def save_df(self, df):
        path = os.path.join("vitivinicultura-api", "data")
        os.makedirs(path, exist_ok=True)
        filepath = os.path.join(path, "tabela_processamento.csv")
        df.to_csv(filepath, index=False)

    def get_json(self):
        """
        Attempts to fetch and clean importation data from Embrapa.
        Falls back to loading local CSV if scraping fails.

        Returns:
            list[dict]: JSON-serializable data.
        """
        try:
            self.get_year()
            df = self.processing_table()
            if df.empty:
                return []
            df = self.encode_latin1(df)
            df = self.clean_quantities(df)
            df = self.categorize(df)
            df = self.remove_categories(df)
            df = self.remove_nan(df)
            df = self.remove_total(df)
            df = self.suboptions_labeling(df)
            self.save_df(df)

            return df.to_dict(orient="records")

        except Exception as e:
            print(
                f"[WARN] Scraper failed. Falling back to local CSV. "
                f"Reason: {e}"
            )
            try:
                df_fallback = pd.read_csv(
                    "vitivinicultura-api/data/tabela_processamento.csv"
                )
                return df_fallback.to_dict(orient="records")
            except Exception as fallback_error:
                print(f"[ERROR] Failed to load fallback CSV: {fallback_error}")
                return []
