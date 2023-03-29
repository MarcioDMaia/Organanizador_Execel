import pandas as pd
import numpy as np

class ReaderXlsx:

    def __init__(self, route, choice, name):
        self.df = pd.read_excel(route)
        self.names_column = [column for column in self.df]
        self.all_lines = np.array([choice])
        self.new_df = {column:np.array([]) for column in self.names_column}
        self.name = name


    def filter(self, type="PRODUTO QUÍMICO"):
        """ Reorganiza a planilha como desejado
            Entrada: type (:= Nome da coluna que se deseja começar)
            Saída: null
        """

        # Encontra todas as variáveis da coluna que se dejesa analisar

        for line  in self.df[f"{type}"]:
            # Caso não exista, adiciona o nome da linha nova
            
            if line not in self.all_lines:
                self.all_lines = np.append(self.all_lines, line)

        for i in self.all_lines:
            self.rearrenge(i, type)


    def rearrenge(self, first, type="PRODUTO QUÍMICO"):
        """ Agrupa todas as linhas desejadas com o parametro sendo o primeiro a ocorrer
        """

        # Reorganiza a tabela
        for index_line in range(len(self.df)):
            if self.df.loc[index_line][type] == first:
                for index, column in enumerate(self.names_column):
                    self.new_df[column] = np.append(self.new_df[column], self.df.loc[index_line][index])
        
                        
    def to_convert(self):
        self.new_df = pd.DataFrame(self.new_df)
        self.new_df.to_excel(self.name)


if __name__ == "__main__":
    df = ReaderXlsx("TestDataframe.xlsx","CLORETO DE POLIALUMÍNIO (PAC-23)", "lui.xlsx")
    df.filter()
    df.to_convert()
