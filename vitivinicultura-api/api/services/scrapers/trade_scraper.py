import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import os


class TradeScraper:
    def __init__(self):
        self.years = None

    def sync(self, base_url, file_path, file_name):
        """
        Main method to execute the trade data scraping workflow.
        It fetches the data, processes it, and saves it as CSV and JSON.

        Args:
            base_url (str): Base URL to scrape data from.
            file_path (str): Directory path where files will be saved.
            file_name (str): Name of the output files (without extension).

        Returns:
            bool: True if sync succeeded and data was saved, False otherwise.
        """
        try:
            self._get_year(base_url)
            df = self._trade_table(base_url)
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
        """
        Extracts the min and max year range available for scraping
        from the input field in the HTML.
        """
        try:
            response = requests.get(base_url + "?opcao=opt_04")
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

    def _trade_table(self, base_url):
        """
        Fetches HTML tables for each available year and combines them.

        Returns:
            pd.DataFrame: Combined DataFrame for all years.
        """
        dfs = []

        for year in self.years:
            url = f"{base_url}?ano={year}&opcao=opt_04"
            try:
                print(f"Requesting {url}...")
                df_year = pd.read_html(url)[3]
                df_year["ano"] = year
                dfs.append(df_year)
            except Exception as e:
                print(f"Error in {year}: {e}")
                raise

        if not dfs:
            return pd.DataFrame()

        df_final = pd.concat(dfs, ignore_index=True)

        if "Unnamed: 2" in df_final.columns:
            df_final = df_final.drop(columns="Unnamed: 2")

        return df_final

    def _encode_latin1(self, df):
        """
        Re-encodes the 'Produto' column from Latin-1 to UTF-8 to fix
            encoding issues.
        """
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

    def _clean_quantities(self, df):
        """
        Normalizes the 'Quantidade (L.)' column by removing separators,
        converting to numbers, and replacing dashes with zeros.
        """
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

    def _categorize(self, df: pd.DataFrame):
        """
        Adds a new column 'Categoria' based on rows where 'Produto'
            is uppercase.
        These are considered headers for subsequent product rows.
        """
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

    def _remove_categories(self, df):
        """
        Removes category rows from the DataFrame, keeping only product rows.

        Returns:
            pd.DataFrame: Filtered DataFrame with only product rows.
        """
        excluded_products = [
            "VINHO FRIZANTE",
            "VINHO ORGÂNICO",
            "SUCO DE UVAS CONCENTRADO",
        ]

        def is_valid_produto(x):
            return (isinstance(x, str) and not x.strip().isupper()) or (
                x.strip() in excluded_products
            )

        mask = df["Produto"].apply(is_valid_produto)
        return df[mask].reset_index(drop=True)

    def _remove_nan(self, df):
        """
        Removes rows containing any NaN values.
        """
        return df.dropna(axis=0)

    def _remove_total(self, df):
        """
        Removes summary rows where 'Produto' is 'Total'.
        """
        return df[df["Produto"] != "Total"]

    def _save_df(self, df, file_path, file_name):
        """
        Saves the cleaned DataFrame as both CSV and JSON files.
        """
        os.makedirs(file_path, exist_ok=True)

        filepath = os.path.join(file_path, f"{file_name}.csv")
        df.to_csv(filepath, index=False)

        filepath_json = os.path.join(file_path, f"{file_name}.json")
        df.to_json(filepath_json, orient="records", force_ascii=False)
