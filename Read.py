import pandas as pd

# Leer el archivo Excel
file_path = "input.xlsx"
data = pd.read_excel(file_path, header=None)  # Leer sin encabezados, ya que no hay uno claro

# Extraer filas necesarias
rows = data.iloc[0:3]  # Filas con t_optimista, t_medio, t_pesimista
rows.columns = data.iloc[3, 1:].values  # Nombres de columnas a partir de las tareas (A, B, C, ...)
rows = rows.iloc[:, 1:]  # Ignorar la primera columna que tiene etiquetas como "t_optimista"

# Transponer y renombrar
tasks = rows.T
tasks.columns = ['t_o', 't_m', 't_p']  # Renombrar columnas
tasks.reset_index(inplace=True)
tasks.rename(columns={'index': 'Tarea'}, inplace=True)

# Convertir a valores numéricos
tasks['t_o'] = pd.to_numeric(tasks['t_o'], errors='coerce')
tasks['t_m'] = pd.to_numeric(tasks['t_m'], errors='coerce')
tasks['t_p'] = pd.to_numeric(tasks['t_p'], errors='coerce')

# Calcular PERT
tasks['D_e'] = (tasks['t_o'] + 4 * tasks['t_m'] + tasks['t_p']) / 6
tasks['sigma^2'] = ((tasks['t_p'] - tasks['t_o']) / 6) ** 2

# Mostrar el resultado
print("Datos con cálculos PERT:")
print(tasks[['Tarea', 't_o', 't_m', 't_p', 'D_e', 'sigma^2']])
