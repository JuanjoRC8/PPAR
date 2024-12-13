
def numero_a_letra(numero, fila_inicio):
    """
    Convierte un número en una letra, comenzando con 'A' para fila_inicio + 1.
    
    Args:
        numero (int): El número que se quiere convertir.
        fila_inicio (int): La fila inicial que se mapea antes de empezar con 'A'.
        
    Returns:
        str: La letra correspondiente al número.
    Llega hasta la letra Z que es lo mismo que el 32
    """
    # Calcular el índice basado en la fila_inicio
    indice = numero - (fila_inicio + 1)
    # Convertir el índice a una letra del alfabeto (A=0, B=1, ..., Z=25)
    if 0 <= indice < 26:  # Asegurarse de que esté en el rango de letras
        return chr(65 + indice)  # 65 es el código ASCII de 'A'
    else:
        return None  # Devolver None si el índice está fuera del rango

def letra_a_numero(numero):
    """
    Convierte una letra en un número, comenzando con 'A' para 1.
    
    Args:
        letra (str): La letra que se quiere convertir.
        
    Returns:
        int: El número correspondiente a la letra.
    """
    # Convertir la letra a un índice (A=0, B=1, ..., Z=25)
    if len(numero) == 1 and "A" <= numero <= "Z":
        return ord(numero) - 65  # 65 es el código ASCII de 'A'
    else:
        return None  # Devolver None si la letra no es válida



def generar_aristas(df):
    """""
    Formato de df:
    df = {
            "A" : {"duracion": 3, "depende_de": []},
            "B" : {"duracion": 4, "depende_de": ["A"]},
            "C" : {"duracion": 2, "depende_de": ["A"]},
    }

    Formato de artistas:
    artistas = {
            1 : {tupla : (1,2), actividad : "A"},
            2 : {tupla : (1,3), actividad : "B"},
            3 : {tupla : (2,4), actividad : "C"},
    """""
    aristas = {}
    n = 0  # Para numerar las aristas de forma secuencial
    actFicticias = 0
    nInd=0
    # Iterar sobre las filas del DataFrame, asumiendo que las dependencias están en pares de filas
    for i in df.keys():
        # Generar los nodos sin depencia
        if df[i]["depende_de"] == []:
           aristas[nInd]= {"tupla" : (0,n+1), "actividad" : i}
           nInd+=1
        
        # Generar los nodos con una dependencia
        elif len(df[i]["depende_de"]) == 1:
            it=1
            conseguido=False
            while (it< len(aristas) and  not conseguido):
                if df[i]["depende_de"][0] == aristas[it]["actividad"]:
                    tupla = aristas[it]["tupla"]
                    aristas[nInd]= {"tupla" : (tupla[1],n+1), "actividad" : i}
                    nInd+=1
                    conseguido=True
                it+=1
            
        # Generar los nodos con varias dependencias
        else:
            nodoFinal = []
            for letra in df[i]["depende_de"]:
                for aux1 in range(len(aristas)):
                    if letra == aristas[aux1]["actividad"]:
                        if aristas[aux1]["tupla"][1] not in nodoFinal:
                            nodoFinal.append(aristas[aux1]["tupla"][1])
            nodoFinal.sort()
            for aux2 in range(len(nodoFinal)-1):
                aristas[nInd] = {"tupla": (nodoFinal[aux2], nodoFinal[aux2]+1), "actividad": "F"+str(actFicticias)}
                nInd+=1
                actFicticias += 1
                # IMPORTANTE DEJO ACTIVIDADES FICTICIAS A 1 VALOR DEL QUE ESTA ESCRITO PARA QUE LA PROXIMA SE ESCRIBA BIEN
            aux3=0
            encontrado=False
            while aux3 < len(aristas) and not encontrado:
                # IMPORTANTE RESTO 1 PORQUE EN VERDAD HE ESCRITO HASTA ACTIIDADES FICTICIAS -1
                if aristas[aux3]["actividad"] == "F"+str(actFicticias-1):
                    nodoAux=aristas[aux3]["tupla"][1]
                    aristas[nInd] = {"tupla": (nodoAux, n+1), "actividad": i}
                    nInd+=1
                    encontrado=True

                aux3+=1
        n += 1
    return aristas