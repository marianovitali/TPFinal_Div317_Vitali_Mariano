"""
Modulo auxiliar con funciones utilitarias para manejo de archivos, cartas y configuraciones.
Incluye funciones para parseo de datos, carga de rankings, generacion de base de datos de cartas y redimensionamiento de imagenes.
"""

import modules.variables as var
import json
import os
import pygame as pg

def parsear_entero(valor: str) -> int:
    """
    Convierte una cadena a entero si contiene solo digitos.
    
    Args:
        valor: Cadena de texto a convertir
        
    Returns:
        int: Numero entero si es valido, caso contrario retorna el valor original
    """
    if valor.isdigit():
        return int(valor)
    return valor

def mapear_valores(matriz: list[list], columna_a_mapear: int, callback):
    """
    Aplica una funcion callback a todos los valores de una columna especifica en una matriz.
    
    Args:
        matriz: Matriz de datos a modificar
        columna_a_mapear: Indice de la columna que se va a transformar
        callback: Funcion que se aplicara a cada valor de la columna
        
    Returns:
        None: Modifica la matriz directamente
    """
    for indice_fila in range(len(matriz)):
        valor = matriz[indice_fila][columna_a_mapear]
        matriz[indice_fila][columna_a_mapear] = callback(valor)

def cargar_ranking(file_path: str, top: int = 10):
    """
    Carga el ranking de puntajes desde un archivo CSV y retorna los mejores puntajes ordenados.
    
    Args:
        file_path: Ruta del archivo CSV con el ranking
        top: Cantidad maxima de registros a retornar (por defecto 10)
        
    Returns:
        list: Lista con los mejores puntajes ordenados de mayor a menor
    """
    ranking = []

    with open(file_path, 'r', encoding='utf-8') as file:
        texto = file.read()

        for linea in texto.split('\n'):
            if linea:
                lista_datos_linea = linea.split(',')
                ranking.append(lista_datos_linea)

    mapear_valores(ranking, columna_a_mapear=1, callback=parsear_entero)

    ranking = ranking[1:]
    ranking.sort(key=lambda fila: fila[1], reverse=True)
    return ranking[:top]

def cargar_configs(file_path: str) -> dict:
    """
    Carga configuraciones desde un archivo JSON.
    
    Args:
        file_path: Ruta del archivo JSON con las configuraciones
        
    Returns:
        dict: Diccionario con las configuraciones cargadas
    """
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def cargar_configs_stage(stage_data: dict):
    """
    Carga las configuraciones especificas de un nivel en los datos del stage.
    
    Args:
        stage_data: Diccionario con los datos del nivel actual
        
    Returns:
        None: Modifica el diccionario stage_data directamente
    """
    if not stage_data.get('juego_finalizado') and not stage_data.get('data_cargada'):
        configs_globales = cargar_configs(var.JSON_CONFIGS)
        nro_stage = stage_data.get('nro_stage')
        stage_data['configs'] = configs_globales.get(f'nivel_{nro_stage}')
        
        if stage_data.get('configs'):
            stage_data['ruta_mazo'] = stage_data.get('configs').get('ruta_mazo')
            stage_data['nombre_mazo_jugador'] = stage_data.get('configs').get('mazo_player')
            stage_data['nombre_mazo_enemigo'] = stage_data.get('configs').get('mazo_enemigo')
            stage_data['coords_inicial_mazo_enemigo'] = stage_data.get('configs').get('coordenada_mazo_enemigo')
            stage_data['coords_inicial_mazo_player'] = stage_data.get('configs').get('coordenada_mazo_player')
            stage_data["cantidad_cartas_jugadores"] = stage_data.get('configs').get('cantidad_cartas_jugadores')

def guardar_info_csv(informacion: str):
    """
    Agrega informacion de puntaje al archivo CSV del ranking.
    
    Args:
        informacion: Cadena de texto con los datos a guardar en formato CSV
        
    Returns:
        None
    """
    with open(var.RANKING_CSV, 'a', encoding='utf-8') as file:
        file.write(informacion)
        print('Informacion guardada en el archivo CSV.')

def parsear_datos_carta(filename: str) -> dict:
    """
    Extrae las estadisticas de una carta parseando el nombre del archivo.
    
    Args:
        filename: Nombre del archivo de la carta con formato especifico
        
    Returns:
        dict: Diccionario con los atributos de la carta (id, atk, def, hp, estrellas)
    """
    """Parsea el nombre del archivo y extrae los stats de la carta.
    Formato esperado: '0.0.1_HP_3800_ATK_4300_DEF_2900_3'"""
    partes = filename.replace('.png', '').split('_')
    
    # Buscar HP, ATK, DEF
    hp = 0
    atk = 0
    def_val = 0
    
    for i in range(len(partes)):
        if partes[i] == 'HP' and i + 1 < len(partes):
            hp = int(partes[i + 1])
        elif partes[i] == 'ATK' and i + 1 < len(partes):
            atk = int(partes[i + 1])
        elif partes[i] == 'DEF' and i + 1 < len(partes):
            def_val = int(partes[i + 1])
    
    # Extraer estrellas 
    estrellas = int(partes[-1]) if partes[-1].isdigit() else 0
    
    return {
        'id': partes[0],
        'atk': atk,
        'def': def_val,
        'hp': hp,
        'estrellas': estrellas
    }

def generar_bd_cartas(path_mazo: str) -> dict:
    """
    Genera una base de datos de cartas escaneando los directorios de mazos y parseando los nombres de archivo.
    
    Args:
        path_mazo: Ruta del directorio que contiene los mazos de cartas
        
    Returns:
        dict: Diccionario con todas las cartas organizadas por mazo
    """
    cartas_dict = {
        "cartas": {}
    }

    for root, dir, files in os.walk(path_mazo):
        reverse_path = ''
        deck_cards = []
        deck_name = root.replace('\\', '/').split('/')[-1]
        for carta in files:
            card_path = os.path.join(root, carta)
            print(f'DECK NAME: {deck_name}')

            if 'reverse' in card_path:
                reverse_path = card_path.replace('\\', '/')
            else:
                card_path = card_path.replace('\\', '/')
                
                datos_card = parsear_datos_carta(carta)
                datos_card['ruta_frente'] = card_path
                datos_card['ruta_reverso'] = ''
                
                deck_cards.append(datos_card)
        for index_carta in range(len(deck_cards)):
            deck_cards[index_carta]['ruta_reverso'] = reverse_path
        
        if deck_name:
            cartas_dict['cartas'][deck_name] = deck_cards
    
    return cartas_dict

def guardar_info_cartas(ruta_archivo: str, dict_cards: dict):
    """
    Guarda la informacion de las cartas en un archivo JSON.
    
    Args:
        ruta_archivo: Ruta donde se guardara el archivo JSON
        dict_cards: Diccionario con la informacion de todas las cartas
        
    Returns:
        None
    """
    with open(ruta_archivo, 'w', encoding='utf-8') as file:
        json.dump(dict_cards, file, indent=4)

def cargar_y_preparar_mazos(stage_data: dict):
    """
    Carga los mazos del jugador y enemigo y los inicializa en el mazo completo del stage.
    
    Args:
        stage_data: Diccionario con los datos del nivel actual
        
    Returns:
        None: Modifica stage_data agregando las cartas al mazo_completo
    """
    """Carga los mazos de jugador y enemigo directamente en mazo_completo"""
    if not stage_data.get('juego_finalizado'):
        if os.path.exists(var.JSON_INFO_CARDS) and os.path.isfile(var.JSON_INFO_CARDS):
            print('+++++ Cargando base de datos de cartas desde archivo... +++++')
            cartas = cargar_configs(var.JSON_INFO_CARDS)
        else:
            print('====== Generando base de datos de cartas desde directorio... ======')
            cartas = generar_bd_cartas(stage_data.get('ruta_mazo'))
            guardar_info_cartas(var.JSON_INFO_CARDS, cartas)
        
        # Obtener cartas de ambos mazos
        cartas_enemigo = cartas.get('cartas').get(stage_data.get('nombre_mazo_enemigo'), [])
        cartas_jugador = cartas.get('cartas').get(stage_data.get('nombre_mazo_jugador'), [])
        
        # Inicializar y agregar todas las cartas al mazo completo
        from modules.carta import inicializar_carta
        for carta_data in cartas_jugador:
            carta_init = inicializar_carta(carta_data, (0, 0))
            stage_data['mazo_completo'].append(carta_init)
        
        for carta_data in cartas_enemigo:
            carta_init = inicializar_carta(carta_data, (0, 0))
            stage_data['mazo_completo'].append(carta_init)

def redimesionar_imagen(ruta_img: str, porcentaje_a_ajustar: int):
    """
    Redimensiona una imagen aplicando un porcentaje de escala.
    
    Args:
        ruta_img: Ruta de la imagen a redimensionar
        porcentaje_a_ajustar: Porcentaje de escala a aplicar (50 significa 50%)
        
    Returns:
        Surface: Imagen redimensionada de Pygame
    """
    image_raw = pg.image.load(ruta_img)
    ancho = image_raw.get_width()
    alto = image_raw.get_height()

    nuevo_alto = int(alto * float(f'0.{porcentaje_a_ajustar}'))
    nuevo_ancho = int(ancho * float(f'0.{porcentaje_a_ajustar}'))

    imagen_final = pg.transform.scale(image_raw, (nuevo_ancho, nuevo_alto))
    return imagen_final


def reducir(callback, iterable: list):
    """
    Aplica una funcion callback recursivamente a todos los elementos de una lista y suma los resultados.
    
    Args:
        callback: Funcion que se aplicara a cada elemento
        iterable: Lista de elementos a procesar
        
    Returns:
        int: Suma total de los valores retornados por el callback
    """
    if not iterable:  # Caso base: lista vacia
        return 0
    # Caso recursivo: primer elemento + reducir el resto
    return callback(iterable[0]) + reducir(callback, iterable[1:])

