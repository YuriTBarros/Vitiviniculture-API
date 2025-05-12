import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import os


class ExportationScraper:
    def __init__(self):
        self.years = None  # List of available years to scrape

    def sync(self, base_url, file_path, file_name):
        """
        Main method to execute the exportation scraping workflow.
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
            df = self._exportation_table(base_url)
            if df.empty:
                return False

            # Processing pipeline
            df = self._encode_latin1(df)
            df = self._clean_quantities_and_values(df)
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
        """
        Fetches the available year range for data scraping from the base page.
        """
        try:
            response = requests.get(f"{base_url}?opcao=opt_06", timeout=10)
            response.raise_for_status()
        except RequestException as e:
            print(f"[ERROR] Failed to connect to Embrapa: {e}")
            self.years = []
            raise

        soup = BeautifulSoup(response.content, "html.parser")
        select_years = soup.find("input", {"class": "text_pesq"})
        self.years = list(
            range(int(select_years["min"]), int(select_years["max"]) + 1)
        )

    def _remove_categories(self, df):
        """
        Removes rows where 'Países' is in uppercase (likely category headers).
        """
        if "Países" not in df.columns:
            return df
        mask = df["Países"].apply(
            lambda x: isinstance(x, str) and not x.strip().isupper()
        )
        return df[mask].reset_index(drop=True)

    def _exportation_table(self, base_url):
        """
        Collects exportation tables for all years and sub-options.

        Returns:
            DataFrame: Combined data from all sub-options and years.
        """
        dfs = []
        for year in self.years:
            for subop in range(1, 5):
                suboption = f"subopt_0{subop}"
                url = (
                    f"{base_url}?subopcao={suboption}&opcao=opt_06&ano={year}"
                )
                try:
                    print(f"Requesting {url}...")
                    df_year = pd.read_html(url)[3]
                    df_year["ano"] = year
                    df_year["subopcao"] = suboption
                    dfs.append(df_year)
                except Exception as e:
                    print(
                        f"[ERROR] Failed for year {year}, "
                        f"suboption {suboption}: {e}"
                    )
                    raise

        if not dfs:
            return pd.DataFrame()

        df_final = pd.concat(dfs, ignore_index=True)

        # Drop unneeded or malformed columns if they exist
        for col in ["Unnamed: 2", "Sem definiÃ§Ã£o"]:
            if col in df_final.columns:
                df_final = df_final.drop(columns=col)

        # Rename malformed column names
        df_final = df_final.rename(columns={"PaÃ­ses": "Países"})
        return df_final

    def _encode_latin1(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fixes encoding issues in the 'Países' column (Latin1 to UTF-8).
        """

        def try_fix_encoding(x):
            if not isinstance(x, str):
                return x
            try:
                return x.encode("latin1").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                return x

        if "Países" in df.columns:
            df["Países"] = df["Países"].astype(str).apply(try_fix_encoding)
        return df

    def _clean_quantities_and_values(self, df):
        """
        Cleans numeric columns by replacing special characters and converting
            to numbers.
        """
        for col in ["Quantidade (Kg)", "Valor (US$)"]:
            if col in df.columns:
                df[col] = df[col].replace("-", "0")
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(".", "", regex=False)
                    .str.replace("-", "", regex=False)
                    .str.strip()
                )
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    def _remove_nan(self, df):
        """
        Removes rows with any NaN values.
        """
        return df.dropna(axis=0)

    def _remove_total(self, df):
        """
        Removes rows labeled as 'Total' in the 'Países' column.
        """
        return df[df["Países"] != "Total"]

    def _suboptions_labeling(self, df):
        """
        Maps technical suboption codes to human-readable labels.
        """
        labels = {
            "subopt_01": "Vinhos de mesa",
            "subopt_02": "Espumantes",
            "subopt_03": "Uvas frescas",
            "subopt_04": "Uvas passas",
            "subopt_05": "Suco de uva",
        }
        df["subopcao"] = df["subopcao"].map(labels)
        return df

    def _save_df(self, df, file_path, file_name):
        """
        Saves the cleaned DataFrame as both CSV and JSON files.
        """
        os.makedirs(file_path, exist_ok=True)

        filepath = os.path.join(file_path, f"{file_name}.csv")
        df.to_csv(filepath, index=False)

        filepath_json = os.path.join(file_path, f"{file_name}.json")
        df.to_json(filepath_json, orient="records", force_ascii=False)
