import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import os


class ImportationScraper:
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
            # Retrieves the available years for scraping
            self._get_year(base_url)
            # Retrieves the importation table
            df = self._importation_table(base_url)
            if df.empty:
                return False

            # Performs a series of transformations on the data
            df = self._encode_latin1(df)
            df = self._clean_quantities_and_values(df)
            df = self._remove_categories(df)
            df = self._remove_nan(df)
            df = self._remove_total(df)
            df = self._suboptions_labeling(df)

            # Saves the cleaned data in files
            self._save_df(df, file_path, file_name)
            return True

        except Exception as e:
            # In case of an error, print the message and return False
            print(f"[WARN] Scraper failed. Reason: {e}")
            return False

    def _get_year(self, base_url):
        """
        Retrieves the available year range for scraping.

        Args:
            base_url (str): The base URL for scraping data.

        Raises:
            RequestException: If there is an error connecting to the source.
        """
        try:
            # Makes the request to get the available years
            response = requests.get(base_url + "?opcao=opt_05", timeout=10)
            response.raise_for_status()
        except RequestException as e:
            print(f"[ERROR] Failed to connect to Embrapa: {e}")
            self.years = []
            raise

        # Parses the HTML content to extract the years
        soup = BeautifulSoup(response.content, "html.parser")
        select_years = soup.find("input", {"class": "text_pesq"})
        self.years = [
            year
            for year in range(
                int(select_years["min"]), int(select_years["max"]) + 1
            )
        ]

    def _remove_categories(self, df):
        """
        Removes rows that contain irrelevant categories.

        Args:
            df (pd.DataFrame): DataFrame with the importation data.

        Returns:
            pd.DataFrame: Filtered DataFrame without the unwanted categories.
        """
        if "Países" not in df.columns:
            return df
        # Filters rows where the "Países" column has values in lowercase
        #   letters
        mask = df["Países"].apply(
            lambda x: isinstance(x, str) and not x.strip().isupper()
        )
        return df[mask].reset_index(drop=True)

    def _importation_table(self, base_url):
        """
        Extracts the importation table for all years and suboptions.

        Args:
            base_url (str): The base URL for scraping the data.

        Returns:
            pd.DataFrame: DataFrame containing the complete table.
        """
        dfs = []
        for year in self.years:
            for subop in range(1, 6):
                suboption = f"subopt_0{subop}"
                url = (
                    f"{base_url}?subopcao={suboption}"
                    f"&opcao=opt_05"
                    f"&ano={year}"
                )
                try:
                    # Makes the request for each suboption and year
                    print(f"Requesting {url}...")
                    df_year = pd.read_html(url)[
                        3
                    ]  # Extracts the table from the page
                    df_year["ano"] = year
                    df_year["subopcao"] = suboption
                    dfs.append(df_year)
                except Exception as e:
                    print(f"Error in {year}, suboption {suboption}: {e}")
                    raise

        if not dfs:
            return pd.DataFrame()
        df_final = pd.concat(dfs, ignore_index=True)

        # Remove columns 'Unnamed: 2' and/or 'Sem definiÃ§Ã£o' if required
        if "Unnamed: 2" or "Sem definiÃ§Ã£o" in df_final.columns:
            columns_to_remove = ["Unnamed: 2", "Sem definiÃ§Ã£o"]
            df_final = df_final.drop(
                columns=[
                    col for col in columns_to_remove if col in df_final.columns
                ]
            )

        df_final = df_final.rename(columns={"PaÃ­ses": "Países"})
        return df_final

    def _encode_latin1(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Encodes strings in the 'Países' column from Latin1 to UTF-8.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.

        Returns:
            pd.DataFrame: The DataFrame with 'Países' column re-encoded.
        """

        def try_fix_encoding(x):
            if not isinstance(x, str):
                return x
            try:
                return x.encode("latin1").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                return x  # If fails, the original value is returned

        if "Países" in df.columns:
            df["Países"] = df["Países"].astype(str).apply(try_fix_encoding)
        return df

    def _clean_quantities_and_values(self, df):
        """
        Cleans the 'Quantidade (Kg)' and 'Valor (US$)' columns by replacing
            invalid values and formatting.

        Args:
            df (pd.DataFrame): The DataFrame to be cleaned.

        Returns:
            pd.DataFrame: The cleaned DataFrame.
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
        Removes rows containing NaN values.

        Args:
            df (pd.DataFrame): The DataFrame to be cleaned.

        Returns:
            pd.DataFrame: The DataFrame with NaN values removed.
        """
        df = df.dropna(axis=0)
        return df

    def _remove_total(self, df):
        """
        Removes rows where the 'Países' column contains the value 'Total'.

        Args:
            df (pd.DataFrame): The DataFrame to be cleaned.

        Returns:
            pd.DataFrame: The cleaned DataFrame without 'Total' rows.
        """
        df = df[df["Países"] != "Total"]
        return df

    def _suboptions_labeling(self, df):
        """
        Maps suboption codes to human-readable labels.

        Args:
            df (pd.DataFrame): The DataFrame to be labeled.

        Returns:
            pd.DataFrame: The labeled DataFrame.
        """
        map = {
            "subopt_01": "Vinhos de mesa",
            "subopt_02": "Espumantes",
            "subopt_03": "Uvas frescas",
            "subopt_04": "Uvas passas",
            "subopt_05": "Suco de uva",
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
