import pandas as pd
import numpy as np
import warnings
from graph import AllGraphs
warnings.filterwarnings("ignore", category=FutureWarning)

class ReaderXlsx:

    def __init__(self, route):
        self.route = route 
        self.df = pd.read_excel(self.route)
        self.df["TOTAL"] = 0
        self.names_column = self.df.columns
        self.product, self.units, self.new_df, self.total = np.array([]), np.array([]), self.zero_df(), 0
        self.real_columns = [i for i in self.names_column[:6]]
        self.real_columns.append("TOTAL")

        
    def zero_df(self):
        new_df = {column:np.array([]) for column in self.names_column[:6]}
        new_df["TOTAL"] = np.array([])
        return new_df
    
    def all_products(self):
        """ Separa todos os produtos químicos
        """
        # Separa todos os produtos químicos
        for line in self.df.index:
            if (self.df.loc[line]["PRODUTO QUÍMICO"] not in self.product):
                self.product = np.append(self.product, self.df.loc[line]["PRODUTO QUÍMICO"])
        
        return self.product


    def all_units(self, type="PRODUTO QUÍMICO", type_2="HIPOCLORITO DE CÁLCIO"):
        """Separa todos os produtos químicos presentes no arquivo
        """
        
        for line in self.df.index:
            if self.df.loc[line][type] == type_2 and self.df.loc[line]["UNIDADE"] not in self.units:
                self.units = np.append(self.units, self.df.loc[line]["UNIDADE"])
        return self.units
        

    def filter(self, first, unit, type="PRODUTO QUÍMICO", type_2="UNIDADE"):
        """ 

        """
        self.total, total_parcial = 0, 0
        # Percorre todas as linhas da planilha
        for index in self.df.index:
            
            if self.df[type_2][index] == unit and self.df[type][index] == first:
                for column in self.names_column:
                    if column != "TOTAL" and column not in self.names_column[-13:-1]:
                            self.new_df[column] = np.append(self.new_df[column], self.df.loc[index][column])
                            
                    if column in self.names_column[-13:-1] and self.df.loc[index][column] > 0:
                        total_parcial += self.df.loc[index][column]

                    if column == "TOTAL":
                        self.total += total_parcial
                        self.new_df[column] = np.append(self.new_df[column], total_parcial)
                        total_parcial = 0
    
        self.new_line(1)
    
    def DataF(self, df):
        # Cria um data frame pandas

        return pd.DataFrame(df)

    def new_line(self, command=0, times=2):
        match command:
            case 0:
                # Cria uma linha em branco
                for time in range(times):
                    for key, value in self.new_df.items():
                        self.new_df[key] = np.append(self.new_df[key], "")
            case 1:
                # Cria uma linha com o total
                for key, value in self.new_df.items():
                    if key != "TOTAL" and key != "UNIDADE":
                        self.new_df[key] = np.append(self.new_df[key], "")
                    
                    if key == "UNIDADE":
                        self.new_df[key] = np.append(self.new_df[key], "TOTAL")
                    
                    if key == "TOTAL":
                        self.new_df[key] = np.append(self.new_df[key], self.total)

    def loop(self):
        data = {111111111111111111:0}
        counter = 0
        # Cria um sheet para cada produto químico com o total de cada
        for products in self.all_products():
            for units in self.all_units():
                self.filter(first=products, unit=units)
                self.new_line() # Cria duas linhas vazias
            data[counter] = self.new_df
            graph_1 = AllGraphs(data=data[counter], products=self.product, units=self.units)
            counter += 1
            self.to_convert(f"{products}")
            graph_1.Pie_graph(products)
            graph_1.Bar_graph(products)
            if counter == 1:
                graph_1.Line_graph(self.product, self.names_column, self.df, self.units)
        
        



    def to_convert(self, name):
        # Abre o arquivo xlsx para escriva, e cria uma sheet. Depois zera o data frame 
        if (name ==  "CLORETO DE POLIALUMÍNIO (PAC-23)"):
            name = "PAC-23"

        if (name ==  "PASTILHA DE HIPOCLORITO DE CÁLCIO"):
            name = "PASTILHA DE HIPOCLORITO DE CAL"

        self.new_df = self.DataF(self.new_df)

        with pd.ExcelWriter(self.route, mode='a') as writer:
            self.new_df.to_excel(writer, sheet_name=name, index=False)
            self.new_df = self.zero_df()
    

if __name__ == "__main__":
    df = ReaderXlsx("C:/Users/Casa/Desktop/Organizador_planilhas/DataFrame.xlsx")  
    df.loop() # Teste para produtos 