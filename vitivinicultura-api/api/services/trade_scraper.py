import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import os


class TradeScraper:
    def __init__(self):
        self.base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
        self.years = None

    def get_year(self):
        try:
            response = requests.get(self.base_url + "?opcao=opt_04")
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

        for product in df["Produto"]:
            product_str = str(product).strip()

            if product_str.isupper() and product_str not in (
                "NAN",
                "VINHO FRIZANTE",
                "VINHO ORGÂNICO",
                "SUCO DE UVAS CONCENTRADO",
            ):
                current_category = product_str

            categories.append(current_category)

        df["Categoria"] = categories
        return df

        def is_valid_produto(x, excluded_products):
            return (isinstance(x, str) and not x.strip().isupper()) or (
                x.strip() in excluded_products
            )

        def remove_categories(self, df):
            excluded_products = [
                "VINHO FRIZANTE",
                "VINHO ORGÂNICO",
                "SUCO DE UVAS CONCENTRADO",
            ]
            mask = df["Produto"].apply(
                lambda x: is_valid_produto(x, excluded_products)
            )
            return df[mask].reset_index(drop=True)

    def trade_table(self):
        dfs = []

        for year in self.years:
            url = f"{self.base_url}?ano={year}&opcao=opt_04"
            try:
                df_year = pd.read_html(url)[3]
                df_year["ano"] = year
                dfs.append(df_year)
            except Exception as e:
                print(f"Error in {year}: {e}")
        if not dfs:
            return pd.DataFrame()
        df_final = pd.concat(dfs, ignore_index=True)

        # Remove column 'Unnamed: 2' if necessary.
        if "Unnamed: 2" in df_final.columns:
            df_final = df_final.drop(columns="Unnamed: 2")

        # Calls the function Categorize
        df_final = self.categorize(df_final)

        return df_final

    def encode_latin1(self, df):
        if "Produto" in df.columns:
            df["Produto"] = (
                df["Produto"]
                .astype(str)
                .apply(
                    lambda x: (
                        x.encode("latin1").decode("utf-8")
                        if isinstance(x, str)
                        else x
                    )
                )
            )
        return df

    def clean_quantities(self, df):
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

    def remove_nan(self, df):
        df = df.dropna(axis=0)
        return df

    def remove_total(self, df):
        df = df[df["Produto"] != "Total"]
        return df

    def save_df(self, df):
        path = os.path.join("vitivinicultura-api", "data")
        os.makedirs(path, exist_ok=True)
        filepath = os.path.join(path, "tabela_comercio.csv")
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
            df = self.trade_table()
            if df.empty:
                return []
            df = self.encode_latin1(df)
            df = self.clean_quantities(df)
            df = self.categorize(df)
            df = self.remove_categories(df)
            df = self.remove_nan(df)
            df = self.remove_total(df)
            self.save_df(df)

            return df.to_dict(orient="records")

        except Exception as e:
            print(
                f"[WARN] Scraper failed. Falling back to local CSV. "
                f"Reason: {e}"
            )
            try:
                df_fallback = pd.read_csv(
                    "vitivinicultura-api/data/tabela_comercio.csv"
                )
                return df_fallback.to_dict(orient="records")
            except Exception as fallback_error:
                print(f"[ERROR] Failed to load fallback CSV: {fallback_error}")
                return []
