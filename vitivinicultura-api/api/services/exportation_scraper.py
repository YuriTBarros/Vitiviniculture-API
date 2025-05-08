import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import os

class ExportationScraper():
    def __init__(self):
        self.base_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php'
        self.years = None

    def get_year(self):
        try:
            response = requests.get(self.base_url + '?opcao=opt_06', timeout=10)
            response.raise_for_status()
        except RequestException as e:
            print(f"[ERROR] Failed to connect to Embrapa: {e}")
            self.years = []
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        select_years = soup.find('input', {'class':'text_pesq'})
        self.years = [year for year in range(int(select_years['min']), int(select_years['max']) + 1)]

    def remove_categories(self, df):
        if 'Países' not in df.columns:
            return df
        mask = df['Países'].apply(lambda x: isinstance(x, str) and not x.strip().isupper())
        return df[mask].reset_index(drop=True)
    
    def exportation_table(self):
        dfs = []
        for year in self.years:
            for subop in range(1, 5):
                suboption = f"subopt_0{subop}"
                url = f"{self.base_url}?subopcao={suboption}&opcao=opt_06&ano={year}"
                try:
                    df_year = pd.read_html(url)[3]
                    df_year['ano'] = year
                    df_year['subopcao'] = suboption
                    dfs.append(df_year)
                except Exception as e:
                    print(f"Error in {year}, suboption {suboption}: {e}")
       
        if not dfs:
            return pd.DataFrame()  # Return empty DataFrame safely
        df_final = pd.concat(dfs, ignore_index=True)

        # Remove  columns 'Unnamed: 2' and / or 'Sem definiÃ§Ã£o' if required 
        if 'Unnamed: 2' or 'Sem definiÃ§Ã£o' in df_final.columns:
            columns_to_remove = ['Unnamed: 2', 'Sem definiÃ§Ã£o']
            df_final = df_final.drop(columns=[col for col in columns_to_remove if col in df_final.columns])

        df_final = df_final.rename(columns={'PaÃ­ses': 'Países'})
        return df_final
    
    def encode_latin1(self, df: pd.DataFrame) -> pd.DataFrame:
        def try_fix_encoding(x):
            if not isinstance(x, str):
                return x
            try:
                return x.encode('latin1').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                return x  # if fails, original is returned

        if 'Países' in df.columns:
            df['Países'] = df['Países'].astype(str).apply(try_fix_encoding)
        return df

    def clean_quantities_and_values(self, df):
        for col in ['Quantidade (Kg)', 'Valor (US$)']:
            if col in df.columns:
                df[col] = df[col].replace('-', '0')
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace('.', '', regex=False)
                    .str.replace('-', '', regex=False)
                    .str.strip()
                )
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df 
    
    def remove_nan(self, df):
        df = df.dropna(axis=0)
        return df
    
    def remove_total(self, df):
        df = df[df['Países'] != 'Total']
        return df
    
    def suboptions_labeling(self, df):
        map = {
            'subopt_01': 'Vinhos de mesa',
            'subopt_02': 'Espumantes',
            'subopt_03': 'Uvas frescas',
            'subopt_04': 'Uvas passas',
            'subopt_05': 'Suco de uva'
        }
        df['subopcao'] = df['subopcao'].map(map)
        return df
    
    def save_df(self, df):
        path = os.path.join('vitivinicultura-api', 'data')
        os.makedirs(path, exist_ok=True) 
        filepath = os.path.join(path, 'tabela_exportacao.csv')
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
            df = self.exportation_table()
            if df.empty:
                return []
            df = self.encode_latin1(df)
            df = self.clean_quantities_and_values(df)
            df = self.remove_categories(df)
            df = self.remove_nan(df)
            df = self.remove_total(df)
            df = self.suboptions_labeling(df)
            self.save_df(df)

            return df.to_dict(orient="records")

        except Exception as e:
            print(f"[WARN] Scraper failed. Falling back to local CSV. Reason: {e}")
            try:
                df_fallback = pd.read_csv("vitivinicultura-api/data/tabela_exportacao.csv")
                return df_fallback.to_dict(orient="records")
            except Exception as fallback_error:
                print(f"[ERROR] Failed to load fallback CSV: {fallback_error}")
                return []