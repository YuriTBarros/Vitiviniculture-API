import pandas as pd

from scrap_processamento import ScraperProcessamento
from scrap_comercio import ScraperComercio
from scrap_producao import ScraperProducao
from scrap_importacao import ScraperImportacao
from scrap_exportacao import ScraperExportacao


class Orchestrator():
    def exec_processamento(self):
        try:
            df_processamento = ScraperProcessamento().exec()
            return df_processamento
        except Exception as e:
            df_processamento = pd.read_csv(r'vitivinicultura-api\data\processamento.csv')
            return df_processamento
            
    def exec_comercio(self):
        try:
            df_comercio = ScraperComercio().exec()
            return df_comercio
        except Exception as e:
            df_comercio = pd.read_csv(r'vitivinicultura-api\data\tabela_comercio.csv')
            return df_comercio

    def exec_producao(self):
        try:
            df_producao = ScraperProducao().exec()
            return df_producao
        except Exception as e:
            df_producao = pd.read_csv(r'vitivinicultura-api\data\tabela_producao.csv')
            return df_producao
        
    def exec_importacao(self):
        try:
            df_producao = ScraperImportacao().exec()
            return df_producao
        except Exception as e:
            df_producao = pd.read_csv(r'vitivinicultura-api\data\tabela_importacao.csv')
            return df_producao
        
    def exec_exportacao(self):
        try:
            df_producao = ScraperExportacao().exec()
            return df_producao
        except Exception as e:
            df_producao = pd.read_csv(r'vitivinicultura-api\data\tabela_exportacao.csv')
            return df_producao
        
    def exec(self):
        self.exec_processamento()
        self.exec_comercio()
        self.exec_producao()
        self.exec_importacao()
        self.exec_exportacao()