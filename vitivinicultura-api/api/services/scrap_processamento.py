import pandas as pd
import requests
from bs4 import BeautifulSoup

class ScraperProcessamento():
    def __init__(self):
        self.base_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php'
        self.anos = None

    def get_year(self):
        response = requests.get(self.base_url + '?opcao=opt_03')
        soup = BeautifulSoup(response.content, 'html.parser')
        select_anos = soup.find('input', {'class':'text_pesq'})
        self.anos = [ano for ano in range(int(select_anos['min']), int(select_anos['max']) + 1)]
        
    def categorizar(self, df: pd.DataFrame):
        categoria_atual = None
        categorias = []

        for produto in df['Cultivar']:
            produto_str = str(produto).strip()

            if produto_str.isupper() and produto_str != 'NAN':
                categoria_atual = produto_str

            categorias.append(categoria_atual)

        df['Categoria'] = categorias
        return df

    def remover_categorias(self, df):
        mask = df['Cultivar'].apply(lambda x: isinstance(x, str) and not x.strip().isupper())
        return df[mask].reset_index(drop=True)
    
    def table_processamento(self):
        dfs = []
        for ano in self.anos:
            for subop in range(1, 5):  # subopt_01 a subopt_04
                subopcao = f"subopt_0{subop}"
                url = f"{self.base_url}?subopcao={subopcao}&opcao=opt_03&ano={ano}"
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
            # Remove colunas desnecessárias ou corrompidas
            colunas_a_remover = ['Unnamed: 2', 'Sem definiÃ§Ã£o']
            df_final = df_final.drop(columns=[col for col in colunas_a_remover if col in df_final.columns])


        # Chama a função de categorização
        df_final = self.categorizar(df_final)

        return df_final

    
    def encode_latin1(self, df: pd.DataFrame) -> pd.DataFrame:
        def try_fix_encoding(x):
            if not isinstance(x, str):
                return x
            try:
                # Tenta decodificar de latin1 para utf-8 apenas se fizer sentido
                return x.encode('latin1').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                return x  # Retorna original se falhar

        df['Cultivar'] = df['Cultivar'].astype(str).apply(try_fix_encoding)
        return df

    def replace_quantidade(self, df):
        df['Quantidade (Kg)'] = df['Quantidade (Kg)'].replace('-','0')
        return df['Quantidade (Kg)'] 

    def column_to_numeric(self, df):
        df['Quantidade (Kg)'] = (
            df['Quantidade (Kg)']
            .astype(str)
            .str.replace('.', '', regex=False)
            .str.replace('-', '', regex=False)
            .str.strip()
        )

        df['Quantidade (Kg)'] = pd.to_numeric(df['Quantidade (Kg)'], errors='coerce')
        return df['Quantidade (Kg)'] 
    
    def remover_nan(self, df):
        df = df.dropna(axis=0)
        return df
    
    def remover_total(self, df):
        df = df[df['Cultivar'] != 'Total']
        return df
    
    def nomear_subopcoes(self, df):
        mapeamento = {
            'subopt_01': 'Viníferas',
            'subopt_02': 'Americanas e híbridas',
            'subopt_03': 'Uvas de mesa',
            'subopt_04': 'Sem classificação'
        }
        df['subopcao'] = df['subopcao'].map(mapeamento)
        return df

    def save_df(self, df):
        df.to_csv(r'vitivinicultura-api\data\tabela_processamento.csv', index=False)

    def exec(self):
        self.get_year()
        df = self.table_processamento()
        df = self.encode_latin1(df)
        df['Quantidade (Kg)'] = self.replace_quantidade(df)
        df['Quantidade (Kg)'] = self.column_to_numeric(df)
        df = self.categorizar(df)
        df = self.remover_categorias(df)
        df = self.remover_nan(df)
        df = self.remover_total(df)
        df = self.nomear_subopcoes(df)
        self.save_df(df)
        return df

run = ScraperProcessamento()
run.exec()
print('Processamento executado')