import pandas as pd
import requests
from bs4 import BeautifulSoup

class ScraperImportacao():
    def __init__(self):
        self.base_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php'
        self.anos = None

    def get_year(self):
        response = requests.get(self.base_url + '?opcao=opt_05')
        soup = BeautifulSoup(response.content, 'html.parser')
        select_anos = soup.find('input', {'class':'text_pesq'})
        self.anos = [ano for ano in range(int(select_anos['min']), int(select_anos['max']) + 1)]

    def remover_categorias(self, df):
        mask = df['Países'].apply(lambda x: isinstance(x, str) and not x.strip().isupper())
        return df[mask].reset_index(drop=True)
    
    def table_importacao(self):
        dfs = []
        for ano in self.anos:
            for subop in range(1, 6):
                subopcao = f"subopt_0{subop}"
                url = f"{self.base_url}?subopcao={subopcao}&opcao=opt_05&ano={ano}"
                try:
                    df_ano = pd.read_html(url)[3]
                    df_ano['ano'] = ano
                    df_ano['subopcao'] = subopcao
                    dfs.append(df_ano)
                except Exception as e:
                    print(f"Erro no ano {ano}, subopcao {subopcao}: {e}")
        
        df_final = pd.concat(dfs, ignore_index=True)

        # Remove a coluna desnecessária, se existir
        if 'Unnamed: 2' or 'Sem definiÃ§Ã£o' in df_final.columns:
            colunas_a_remover = ['Unnamed: 2', 'Sem definiÃ§Ã£o']
            df_final = df_final.drop(columns=[col for col in colunas_a_remover if col in df_final.columns])

        df_final = df_final.rename(columns={'PaÃ­ses': 'Países'})
        return df_final
    
    def encode_latin1(self, df: pd.DataFrame) -> pd.DataFrame:
        def try_fix_encoding(x):
            if not isinstance(x, str):
                return x
            try:
                return x.encode('latin1').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                return x  # Retorna original se falhar

        df['Países'] = df['Países'].astype(str).apply(try_fix_encoding)
        return df

    def replace_quantidade(self, df):
        df['Quantidade (Kg)'] = df['Quantidade (Kg)'].replace('-','0')
        df['Valor (US$)'] = df['Valor (US$)'].replace('-','0')
        return df['Quantidade (Kg)'], df['Valor (US$)']

    def column_to_numeric(self, df):
        df['Quantidade (Kg)'] = (
            df['Quantidade (Kg)']
            .astype(str)
            .str.replace('.', '', regex=False)
            .str.replace('-', '', regex=False)
            .str.strip()
        )
        df['Quantidade (Kg)'] = pd.to_numeric(df['Quantidade (Kg)'], errors='coerce')

        df['Valor (US$)'] = (
            df['Valor (US$)']
            .astype(str)
            .str.replace('.', '', regex=False)
            .str.replace('-', '', regex=False)
            .str.strip()
        )
        df['Valor (US$)'] = pd.to_numeric(df['Valor (US$)'], errors='coerce')
        return df['Quantidade (Kg)'], df['Valor (US$)'] 
    
    def remover_nan(self, df):
        df = df.dropna(axis=0)
        return df
    
    def remover_total(self, df):
        df = df[df['Países'] != 'Total']
        return df
    
    def nomear_subopcoes(self, df):
        mapeamento = {
            'subopt_01': 'Vinhos de mesa',
            'subopt_02': 'Espumantes',
            'subopt_03': 'Uvas frescas',
            'subopt_04': 'Uvas passas',
            'subopt_05': 'Suco de uva'
        }
        df['subopcao'] = df['subopcao'].map(mapeamento)
        return df

    def save_df(self, df):
        df.to_csv(r'vitivinicultura-api\data\tabela_importacao.csv', index=False)

    def exec(self):
        self.get_year()
        df = self.table_importacao()
        df = self.encode_latin1(df)
        df['Quantidade (Kg)'], df['Valor (US$)'] = self.replace_quantidade(df)
        df['Quantidade (Kg)'], df['Valor (US$)'] = self.column_to_numeric(df)
        df = self.remover_categorias(df)
        df = self.remover_nan(df)
        df = self.remover_total(df)
        df = self.nomear_subopcoes(df)
        self.save_df(df)
        return df


run = ScraperImportacao()
run.exec()
print('Importação executado')