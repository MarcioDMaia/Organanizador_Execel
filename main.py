import matplotlib.pyplot as plt

# Crie um gráfico de exemplo
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [2, 4, 1], label="Exemplo de dados")

# Oculte a legenda de dentro do gráfico
ax.get_legend().set_visible(False)

# Exiba o gráfico
plt.show()
