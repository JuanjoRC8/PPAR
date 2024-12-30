import re

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from funciones_auxiliares import (generar_aristas, letra_a_numero,
                                  numero_a_letra)

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
with open("archivo.tex", "w",encoding="utf-8") as archivo:
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
    if aristas[i]["actividad"] in duraciones.keys():
        G.add_edge(aristas[i]["tupla"][0], aristas[i]["tupla"][1],actividad=aristas[i]["actividad"])
    else:
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

    
# Calcular Early Times (Tiempos más tempranos) manualmente
early_times = [-1]*nNodos  # Empieza en el nodo inicial con tiempo temprano cero
for nodo in nodos:
    if nodo ==0:
        early_times[nodo] = 0
        with open("archivo.tex", "a",encoding="utf-8") as archivo:
            archivo.write(f"$E_{nodo} = {0}$\n")
    else:
        with open("archivo.tex", "a",encoding="utf-8") as archivo:
            archivo.write(f"$E_{nodo} = Max \\{{")
            contador =sum(1 for arista, valor in aristas.items() if valor["tupla"][1] == nodo)
            for arista,valor in aristas.items():
                if valor["tupla"][1] == nodo:
                    archivo.write(f"E_{nodo} + {valor["actividad"]}")
                    contador=contador-1
                    if contador > 0:
                        archivo.write(", ")
                    if re.match(r'^F\d+', valor["actividad"]):
                        auxVal= 0+early_times[valor["tupla"][0]]
                        if early_times[nodo] == -1 or early_times[nodo] < auxVal:
                            early_times[nodo] = auxVal
                    else:
                        auxVal=duraciones[valor["actividad"]]+early_times[valor["tupla"][0]]
                        if early_times[nodo] == -1 or early_times[nodo] < auxVal:
                            early_times[nodo] = auxVal
                            
            archivo.write(f"\\}} = {early_times[nodo]}$\n")
    
#Calculos de los last times (Tiempos mas tardios)
last_times= [-1]*nNodos
for nodo in reversed(nodos):
    if nodo == nNodos-1:
        last_times[nodo] = early_times[nodo]
        with open("archivo.tex", "a",encoding="utf-8") as archivo:
            archivo.write(f"$L_{nodo} = E_{nodo} = {early_times[nodo]}$\n")
    else:
        with open("archivo.tex", "a",encoding="utf-8") as archivo:
            archivo.write(f"$L_{nodo} = Min \\{{")
            contador =sum(1 for arista, valor in aristas.items() if valor["tupla"][0] == nodo)
            for arista,valor in aristas.items():
                if valor["tupla"][0] == nodo:
                    archivo.write(f"L_{valor["tupla"][1]} - {valor["actividad"]}")
                    contador=contador-1
                    if contador > 0:
                        archivo.write(", ")
                    if re.match(r'^F\d+', valor["actividad"]):
                        auxVal= last_times[valor["tupla"][1]]
                        if last_times[nodo] == -1 or last_times[nodo] > auxVal:
                            last_times[nodo] = auxVal
                    else:
                        auxVal=last_times[valor["tupla"][1]] - duraciones[valor["actividad"]]
                        if last_times[nodo] == -1 or last_times[nodo] > auxVal:
                            last_times[nodo] = auxVal
                            
            archivo.write(f"\\}} = {last_times[nodo]}$\n")

with open("archivo.tex", "a",encoding="utf-8") as archivo:
    archivo.write("\n\n\n\n")

#Tabla de earlies y last times
with open("archivo.tex", "a",encoding="utf-8") as archivo:
    archivo.write("\\begin{table}[]\n")
    archivo.write("\\begin{tabular}{lll}\n")
    archivo.write("$t_i$ & $E_i$ & $L_i$ \\\\\n")
    for nodo in nodos:
        archivo.write(f"{nodo} & {early_times[nodo]} & {last_times[nodo]} \\\\\n")
    archivo.write("\\end{tabular}\n")
    archivo.write("\\end{table}\n")

with open("archivo.tex", "a",encoding="utf-8") as archivo:
    archivo.write("\n\n\n\n")
#Calculo de las holguras
holguras = {}
for arista, valor in aristas.items():
    if re.match(r'^F\d+', valor["actividad"]):
        holgura = last_times[valor["tupla"][1]] - early_times[valor["tupla"][0]]
        if holgura < 0.01:  # Comparar con 0.01
            holgura = 0
        holguras[valor["actividad"]] = holgura
        with open("archivo.tex", "a",encoding="utf-8") as archivo:
            archivo.write(f"$H_{valor['actividad']} = L_{valor['tupla'][1]} - E_{valor['tupla'][0]} = {holgura}$\n")
    else:
        holgura = last_times[valor["tupla"][1]] - early_times[valor["tupla"][0]] - duraciones[valor["actividad"]]
        if holgura < 0.01:  # Comparar con 0.01
            holgura = 0
        holguras[valor["actividad"]] = holgura
        with open("archivo.tex", "a",encoding="utf-8") as archivo:
            archivo.write(f"$H_{valor['actividad']} = L_{valor['tupla'][1]} - E_{valor['tupla'][0]} - D_{valor['actividad']} = {holgura}$\n")

with open("archivo.tex", "a",encoding="utf-8") as archivo:
    archivo.write("\n\n\n\n")

# Escribir la tabla en el archivo
with open("archivo.tex", "a",encoding="utf-8") as archivo:
    archivo.write("\\begin{table}[]\n")
    archivo.write("\\begin{tabular}{lllllll}\n")
    archivo.write("Tarea & Ruta   ($i \\longrightarrow j$) & $D_ij$ & $E_i$ & $L_j$ & $H_ij$  = $L_j - E_i - D_ij$ & Crítica \\\\\n")
    
    actividades_keys = list(actividades.keys())  # Convertir a lista para trabajar con índices
    for idx, act in enumerate(actividades_keys):
        archivo.write(f"{act} & ")
        for valor in aristas.values():
            if valor["actividad"] == act:
                archivo.write(f"{valor['tupla'][0]} $\\longrightarrow$ {valor['tupla'][1]} & {duraciones[act]} & {early_times[valor['tupla'][0]]} & {last_times[valor['tupla'][1]]} & {holguras[act]} & ")
                
                # Última iteración del bucle
                if idx == len(actividades_keys) - 1:
                    if holguras[act] == 0:
                        archivo.write("x\n")  # Sin "\\\\" para última iteración
                    else:
                        archivo.write("\n")  # Sin "\\\\" para última iteración
                else:
                    if holguras[act] == 0:
                        archivo.write("x \\\\\n")
                    else:
                        archivo.write(" \\\\\n")
    archivo.write("\\end{tabular}\n")
    archivo.write("\\end{table}\n")



with open("archivo.tex", "a",encoding="utf-8") as archivo:
    archivo.write("\n\n\n\n")
    archivo.write("Caminos críticos:\n")


#Calcular el camino crítico
fin=nNodos-1
caminoCritico =""
for  arista,valor in aristas.items():
    if arista == 0:
        caminoCritico+=valor["actividad"]
        ultimo=valor["tupla"][1]
    if holguras[valor["actividad"]] == 0:
        if valor ["tupla"][1] == fin:
            with  open("archivo.tex", "a",encoding="utf-8") as archivo:
                archivo.write(f"{caminoCritico +"-"+ valor['actividad']}\n")
        if valor["tupla"][0] == ultimo:
            caminoCritico+="-"+valor["actividad"]
            ultimo=valor["tupla"][1]

with open ("archivo.tex", "a",encoding="utf-8") as archivo:
    archivo.write(f"\nDuración del camino crítico: {early_times[nNodos-1]}")

        

