import matplotlib.pyplot as plt
import networkx as nx

# Datos de entrada
actividades = {
    "A": {"duracion": 3, "depende_de": []},
    "B": {"duracion": 4, "depende_de": ["A"]},
    "C": {"duracion": 2, "depende_de": ["A"]},
    "D": {"duracion": 5, "depende_de": ["B", "C"]},
    "E": {"duracion": 1, "depende_de": []}
}

# Crear el grafo dirigido
G = nx.DiGraph()

# Crear nodo inicial
nodo_inicial = 1
G.add_node(nodo_inicial, label="Inicio")

# Crear nodos y aristas basados en dependencias
eventos = {}  # Mapear actividades a nodos de inicio y fin
nodo_actual = 2  # Contador para nodos (inicia después del nodo inicial)
nodos_ficticios = {}  # Para evitar duplicar nodos ficticios con las mismas dependencias

for actividad, datos in actividades.items():
    if not datos["depende_de"]:
        # Si no tiene dependencias, se conecta al nodo inicial
        nodo_inicio = nodo_inicial
    elif len(datos["depende_de"]) == 1:
        # Si tiene una sola dependencia, conectar directamente
        nodo_inicio = eventos[datos["depende_de"][0]][1]
    else:
        # Múltiples dependencias: unificar en un nodo ficticio
        dependencias_clave = tuple(sorted(datos["depende_de"]))
        if dependencias_clave not in nodos_ficticios:
            nodo_ficticio = nodo_actual
            G.add_node(nodo_ficticio, label=f"Ficticio_{nodo_ficticio}")
            nodo_actual += 1
            # Conectar todas las dependencias al nodo ficticio
            for dep in datos["depende_de"]:
                G.add_edge(eventos[dep][1], nodo_ficticio, label=f"Dep_{dep}")
            nodos_ficticios[dependencias_clave] = nodo_ficticio
        nodo_inicio = nodos_ficticios[dependencias_clave]

    # Crear el nodo final de la actividad
    nodo_fin = nodo_actual
    eventos[actividad] = (nodo_inicio, nodo_fin)
    G.add_edge(nodo_inicio, nodo_fin, label=actividad, duracion=datos["duracion"])
    nodo_actual += 1

# Identificar actividades finales (sin sucesores)
todas_dependencias = {dep for datos in actividades.values() for dep in datos["depende_de"]}
actividades_finales = [act for act in actividades.keys() if act not in todas_dependencias]

# Crear el nodo final
nodo_final = nodo_actual
G.add_node(nodo_final, label="Fin")

# Conectar actividades finales al nodo final
for actividad in actividades_finales:
    G.add_edge(eventos[actividad][1], nodo_final, label=f"Fin_{actividad}")

# Dibujar el grafo
pos = nx.spring_layout(G)  # Posicionamiento de nodos
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')

# Etiquetas de las aristas
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

# Mostrar el grafo
plt.title("Diagrama PERT")
plt.show()
