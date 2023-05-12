import openpyxl
import numpy as np
import pandas as pd
from openpyxl.chart import Reference, PieChart
import matplotlib.pyplot as plt
import pickle

class AllGraphs:
    def __init__(self, data, products, units):
        self.data = data        
        self.units = units
        self.products = products    
        self.filtred_data = pd.DataFrame(self.data)[["UNIDADE", "TOTAL"]].to_numpy()
    


    def va_la(self):
        # Produzindo os valores e labels do gráfico de pizza e barras
        values = np.array([float(self.filtred_data[i][1]) for i in np.where(self.filtred_data=="TOTAL")[0]])
        labels = np.array([self.filtred_data[i-1][0] for i in np.where(self.filtred_data=="TOTAL")[0]])

        # Removendo os valores que são iguais a zero e o seu label correspondente
        remove_index = np.where(values==0)
        labels = np.delete(labels, remove_index)
        values = np.delete(values, remove_index)
    
        return [values, labels]

    def Pie_graph(self, product):
        values, labels = self.va_la()

        # Identificando a maior % e criando 
        max_index = np.where(values==np.max(values))[0]
        explode = np.zeros(len(labels))
        np.put(explode, max_index, .2)

        legend = np.array([])
        for i in range(len(values)):
            legend = np.append(legend, f"{labels[i]} - {round((values[i]*100)/np.sum(values), 2)}%")
        np.where(legend==0)
        colors = np.array(["#099aed", "#0689d4", "#056196", "#044f7a", "#023654", "#011f30", "#e03459","#701125","#50eb02","#1c4d04","#820757"])        
        # Crie o gráfico de pizza
        fig, ax = plt.subplots(figsize=(12,5))
        ax.pie(values, 
               labels=None,
               shadow=True, 
               startangle=60, 
               colors=colors,
                explode=explode
                
            )
        ax.set_title(f"{product}", fontsize=12)
        plt.axis("equal")
        plt.tight_layout()
        plt.legend(legend, loc="best")
        name = self.save_fig(fig, product, "pie")

    def save_fig(self, obj, product, type):
        name = f"{product}-{type}"
        obj.savefig(name)
        return name
    
    def Bar_graph(self, product):
        values, labels = self.va_la()

        # Alterando o estilo do gráfico
        
        fig, ax = plt.subplots(figsize=(12,5))
        
        ax.bar(labels, values)

        # Alterando as configurações do gráfico
        ax.set_title(f"{product}")
        ax.set_ylabel("Quantidade total")
        ax.set_xlabel("Unidade")

        # Salvando a imagem e guardando o nome da mesma
        name = self.save_fig(fig, product, "bar")


    def Line_graph(self, products, columns, fullData, units):

        # Reorganiza o df
        sorted_data = fullData.sort_values(by=["UNIDADE","PRODUTO QUÍMICO"])
        

        x_values = columns[-13:-1]
        y_labels = {i : {i: [0 for i in range(12)] for i in products} for i in units}
        
        
        for key_pri in y_labels.keys():
            for key_sec in y_labels[key_pri].keys():
                    values = sorted_data.loc[[i for i in np.where(sorted_data.to_numpy()==key_pri)[0]]] #, [i for i in columns[-13:-1]]

                    for index in range(12):
                        
                        a = sorted_data.loc[[i for i in np.where(values["PRODUTO QUÍMICO"]==key_sec)[0]]]
                        y_labels[key_pri][key_sec][index] = a[[i for i in columns[-13:-1]]].sum()[index]
                       
        colors = ["#b30404", "#0689d4", "#000000", "#91785a", "#fffb00", "#204a44", "#00b1f7", "#071bf2", "#020736", "#ab0990","#bd0868", "#c40434", "#b30715"]
        colors = {products[i]:colors[i] for i in range(len(products))}
        
        for unit in y_labels.keys():
            fig, ax = plt.subplots(figsize=(22, 5))
            for product in y_labels[unit].keys():
                ax.plot(x_values, y_labels[unit][product], color=colors[product])
                ax.hlines(y=sum(y_labels[unit][product])/len(y_labels[unit][product]),xmin=x_values[0], xmax=x_values[-1], color=colors[product])
            ax.set_xlabel("Periodo")
            ax.set_ylabel("Quantidade")
            ax.legend(products, ncol=1, loc="upper right", bbox_to_anchor=(1.2,1))
            self.save_fig(fig, unit, "line")    
            plt.close(fig)
      