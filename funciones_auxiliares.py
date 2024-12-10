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
