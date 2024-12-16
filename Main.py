import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from funciones_auxiliares import generar_aristas, numero_a_letra

# Leer el archivo Excel
file_path = "input.xlsx"
data = pd.read_excel(file_path, sheet_name=0)

# Crear un diccionario para almacenar las duraciones
duraciones = {}
varianzas = {}

# Calcular y almacenar la duración en el diccionario
for col in data.columns[1:]:
    duraciones[col] = (int(data[col].iloc[0]) + 4 * int(data[col].iloc[1]) + int(data[col].iloc[2])) / 6
    varianzas[col] = (int(data[col].iloc[2]) - int(data[col].iloc[0]))**2 / 36

# Crear un fichero y escribir tiempos en el
with open("archivo.txt", "w") as archivo:
    archivo.writelines("\\begin{table}[]\n"
                       "\\begin{tabular}{llllll}\n"
                       "Tarea & $t_o$ & $t_m$ & $t_p$ & $D_e$ & $\\sigma^{2}$ \\\\\n"
                       )
    for tarea in duraciones:
        archivo.write(f"{tarea} & {data[tarea].iloc[0]} & {data[tarea].iloc[1]} & {data[tarea].iloc[2]} & {duraciones[tarea]} & {varianzas[tarea]} \\\\\n")
    archivo.writelines("\\end{tabular}\n"
                       "\\end{table}\n"
                       "\n\n\n\n"
                       )
    
# Inicializar el diccionario de actividades vacío
actividades = {}

for col in data.columns[1:]:
    fila_inicio = 6
    contenido_columna = data[col].iloc[fila_inicio-1:].tolist()

    # Asegurarse de que 'col' tenga su propio diccionario en 'actividades'
    if col not in actividades:
        actividades[col] = {"duracion": duraciones[col], "depende_de": []}

    # Buscar los valores 1 en la columna
    for i, valor in enumerate(contenido_columna):
        if valor == 1:
            # Si la fila 7 siempre será igual a A
            fila_encontrada = fila_inicio + i + 1

            # Asignar la duración y agregar la dependencia a 'depende_de'
            actividades[col]['duracion'] = duraciones[col]  # Asigna la duración
            actividades[col]['depende_de'].append(numero_a_letra(fila_encontrada, fila_inicio))  # Agrega la dependencia

# Generar las aristas del grafo
aristas=generar_aristas(actividades)
#Busco cuantos nodos creo
nNodos=0
auxMax=0
for tupla in aristas:
    for arista in aristas[tupla]["tupla"]:
        if arista>auxMax:
            auxMax=arista
nNodos=auxMax+1 #Porque empiezo en el nodo 0
nodos = list(range(0, nNodos))

# Crear un grafo dirigido y asignar las aristas
G = nx.DiGraph()
G.add_nodes_from(nodos)
for i in range(len(aristas)):
    G.add_edge(aristas[i]["tupla"][0], aristas[i]["tupla"][1],actividad=aristas[i]["actividad"])

# Dibujar el grafo
pos = nx.spring_layout(G)  # Posición de los nodos
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')

# Añadir etiquetas a las aristas
edge_labels = nx.get_edge_attributes(G, 'actividad')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Mostrar el grafo
plt.title("Grafo de Actividades")
plt.savefig("grafo_actividades.png")
plt.show()