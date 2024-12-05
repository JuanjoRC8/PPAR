import pandas as pd
from pulp import LpMinimize, LpProblem, LpVariable, lpSum

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
print("Duraciones: " ,duraciones)
print("Varianzas: " ,varianzas)

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
    
    



