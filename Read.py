import pandas as pd
from pulp import LpMinimize, LpProblem, LpVariable, lpSum

from funciones_auxiliares import letra_a_numero, numero_a_letra

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
    
#CREAR LAS ACTIVIDADES EN UNA VARIABLE
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

# Imprimir el diccionario de actividades
#print(actividades)

# Paso 1: Calcular 'early' (hacia adelante)
for actividad in actividades:
    depende_de = actividades[actividad]["depende_de"]
    if depende_de:  # Si tiene dependencias
        actividades[actividad]["early"] = max(
            actividades[dep]["early"] for dep in depende_de
        ) + actividades[actividad]["duracion"]
        with open("archivo.txt", "a") as archivo:
            archivo.write("$E_{} =  Max \\{{".format(actividad))
            for dep in depende_de:
                archivo.write("E_{} + {}".format(dep,actividad))
                if dep != depende_de[-1]:
                    archivo.write(", ")
            archivo.write("\\}} = {}$\n".format(actividades[actividad]["early"]))
    else:  # Si no tiene dependencias
        actividades[actividad]["early"] = actividades[actividad]["duracion"]
        # Abre el archivo en modo 'append'
        aux_duracion=actividades[actividad]["early"]
        with open("archivo.txt", "a") as archivo:
            archivo.write("$E_{} = {}$\n".format(actividad,aux_duracion))


# Paso 2: Calcular 'late' (hacia atrás)

# Encuentra la duración total del proyecto
proyecto_duracion = max(actividad["early"] for actividad in actividades.values())

# Asigna el valor 'late' inicial para la actividad final
for actividad in actividades:
    if not any(actividad in actividades[a]["depende_de"] for a in actividades):
        actividades[actividad]["late"] = proyecto_duracion
        aux_duracion=actividades[actividad]["late"]
        with open("archivo.txt", "a") as archivo:
            archivo.write("$L_{} = E_{} = {}$\n".format(actividad,actividad,aux_duracion))

# Calcula hacia atrás los valores de 'late'
for actividad in sorted(actividades.keys(), reverse=True):
    if "late" not in actividades[actividad]:
        actividades[actividad]["late"] = min(
            actividades[dep]["late"] - actividades[actividad]["duracion"]
            for dep in actividades
            if actividad in actividades[dep]["depende_de"]
            #TODO revisar que el late esta bien calculado
        )
        with open("archivo.txt", "a") as archivo:
                archivo.write("$L_{} = Min \\{{".format(actividad))
        for dep in actividades:
            if actividad in actividades[dep]["depende_de"]:
                aux_dependencias=actividades[dep]["depende_de"]
                with open("archivo.txt", "a") as archivo:
                    archivo.write("L_{} - {}".format(dep,actividad))
                    if actividad in aux_dependencias[-1]:
                            #TODO no pone bien la coma
                            archivo.write(", ")
        with open("archivo.txt", "a") as archivo:
            archivo.write("\\}} = {}\n".format(actividades[actividad]["late"]))


#TODO ESCRIBIR AQUI LA TABLA DE EARLYS Y LATES

# Paso 3: Calcular la holgura
for actividad in sorted(actividades.keys()):
    holgura=actividades[actividad]["late"] - actividades[actividad]["early"]
    #TODO ESCRIBIR EN EL ARCHIVO LA FORMULA DE LA HOLGURA
    actividades[actividad]["holgura"] =0 if holgura<1e-3 else  holgura

#TODO ESCRIBIR AQUI LA TABLA CON LAS RUTAS 

# Imprimir las actividades con los valores 'early', 'late' y 'holgura'
with open("archivo.txt", "a") as archivo:
    archivo.write("\n\n\n\nRESULT DEBUGGING\n")

for actividad, valores in actividades.items():
    with open("archivo.txt", "a") as archivo:
        archivo.write(f"{actividad}: {valores}\n")
   

#TODO CALCULAR CAMINOS CRITICOS Y DURACIÓN DEL MENOR CAMINO CRITICO