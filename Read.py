import pandas as pd
from pulp import LpMinimize, LpProblem, LpVariable, lpSum

from funciones_auxiliares import numero_a_letra

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

# Imprimir el diccionario de duraciones
#print("Duraciones: " ,duraciones)
#print("Varianzas: " ,varianzas)

# Crear un fichero y escribir contenido en él
with open("mi_archivo.txt", "w") as archivo:
    archivo.writelines("\\begin{table}[] \n"
                       "\\begin{tabular}{llllll} \n"
                       "Tarea & $t_o$ & $t_m$ & $t_p$ & $D_e$ & $\\sigma^{2}$ \\\\ \n"
                       )
    for tarea in duraciones:
        archivo.write(f"{tarea} & {data[tarea].iloc[0]} & {data[tarea].iloc[1]} & {data[tarea].iloc[2]} & {duraciones[tarea]} & {varianzas[tarea]} \\\\ \n")
    archivo.writelines("\\end{tabular} \n"
                       "\\end{table} \n"
                       )
    
#CREAR LAS ACTIVIDADES EN UNA VARIABLE
# Inicializar el diccionario de actividades vacío
actividades = {}

for col in data.columns[1:]:
    fila_inicio = 6
    contenido_columna = data[col].iloc[fila_inicio-1:].tolist()

    # Asegurarse de que 'col' tenga su propio diccionario en 'actividades'
    if col not in actividades:
        actividades[col] = {"duracion": 0, "depende_de": []}

    # Buscar los valores 1 en la columna
    for i, valor in enumerate(contenido_columna):
        if valor == 1:
            # Si la fila 7 siempre será igual a A
            fila_encontrada = fila_inicio + i + 1

            # Asignar la duración y agregar la dependencia a 'depende_de'
            actividades[col]['duracion'] = duraciones[col]  # Asigna la duración
            actividades[col]['depende_de'].append(numero_a_letra(fila_encontrada, fila_inicio))  # Agrega la dependencia

# Imprimir el diccionario de actividades
print(actividades)

        



