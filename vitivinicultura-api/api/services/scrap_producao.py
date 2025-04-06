import pandas as pd
import requests
from bs4 import BeautifulSoup

class ScraperProducao():
    def __init__(self):
        self.base_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php'
        self.anos = None

    def get_year(self):
        response = requests.get(self.base_url + '?opcao=opt_02')
        soup = BeautifulSoup(response.content, 'html.parser')
        select_anos = soup.find('input', {'class':'text_pesq'})
        self.anos = [ano for ano in range(int(select_anos['min']), int(select_anos['max']) + 1)]
        
    def categorizar(self, df: pd.DataFrame):
        categoria_atual = None
        categorias = []

        for produto in df['Produto']:
            produto_str = str(produto).strip()

            if produto_str.isupper() and produto_str != 'NAN':
                categoria_atual = produto_str

            categorias.append(categoria_atual)

        df['Categoria'] = categorias
        return df

    
    def remover_categorias(self, df):
        mask = df['Produto'].apply(lambda x: isinstance(x, str) and not x.strip().isupper())
        return df[mask].reset_index(drop=True)
    
    def table_producao(self):
        dfs = []
        for ano in self.anos:
            url = f"{self.base_url}?ano={ano}&opcao=opt_02"
            try:
                df_ano = pd.read_html(url)[3]
                df_ano['ano'] = ano
                dfs.append(df_ano)
            except Exception as e:
                print(f"Erro no ano {ano}: {e}")
        
        df_final = pd.concat(dfs, ignore_index=True)

        # Remove a coluna desnecessária, se existir
        if 'Unnamed: 2' in df_final.columns:
            df_final = df_final.drop(columns='Unnamed: 2')

        # Chama a função de categorização
        df_final = self.categorizar(df_final)

        return df_final
    
    def encode_latin1(self, df):
        df['Produto'] = df['Produto'].astype(str).apply(
            lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x
        )
        return df  # <- Retornar o DataFrame inteiro

    
    def replace_quantidade(self, df):
        df['Quantidade (L.)'] = df['Quantidade (L.)'].replace('-','0')
        return df['Quantidade (L.)'] 

    def column_to_numeric(self, df):
        df['Quantidade (L.)'] = (
            df['Quantidade (L.)']
            .astype(str)
            .str.replace('.', '', regex=False)
            .str.replace('-', '', regex=False)
            .str.strip()
        )

        df['Quantidade (L.)'] = pd.to_numeric(df['Quantidade (L.)'], errors='coerce')
        return df['Quantidade (L.)'] 
    
    def remover_nan(self, df):
        df = df.dropna(axis=0)
        return df
    
    def remover_total(self, df):
        df = df[df['Produto'] != 'Total']
        return df
    
    def save_df(self, df):
        df.to_csv(r'vitivinicultura-api\data\tabela_producao.csv', index=False)
        
    def exec(self):
        self.get_year()
        df = self.table_producao()
        df = self.encode_latin1(df)
        df['Quantidade (L.)'] = self.replace_quantidade(df)
        df['Quantidade (L.)']  = self.column_to_numeric(df)
        df = self.categorizar(df)
        df = self.remover_categorias(df)
        df = self.remover_nan(df)
        df = self.remover_total(df)
        self.save_df(df)
        return df

run = ScraperProducao()
run.exec()
print('Processamento executado')