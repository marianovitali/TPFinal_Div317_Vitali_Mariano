"""
Modulo para gestion de participantes del juego (jugador y enemigo).
Maneja estadisticas, mazos de cartas, puntajes y renderizado de cada participante.
"""

import pygame as pg
import modules.carta as carta
import modules.variables as var
import modules.auxiliar as aux

def inicializar_participante(pantalla: pg.Surface, nombre: str = 'PC'):
    """
    Crea e inicializa un participante del juego con sus atributos base.
    
    Args:
        pantalla: Superficie de Pygame donde se dibujara el participante
        nombre: Nombre del participante (por defecto 'PC')
        
    Returns:
        dict: Diccionario con todos los atributos del participante inicializados
    """
    player = {}
    player['nombre'] = nombre
    player['hp_inicial'] = 1
    player['hp_actual'] = 1
    player['attack'] = 1
    player['defense'] = 1
    player['score'] = 0
    
    player['mazo_asignado'] = []
    player['cartas_mazo'] = []
    player['cartas_mazo_usadas'] = []

    player['screen'] = pantalla
    player['pos_deck_inicial'] = (0, 0)
    player['pos_deck_jugados'] = (0, 0)


    return player

def get_hp_participante(participante: dict) -> int:
    """
    Obtiene los puntos de vida actuales de un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        int: Puntos de vida actuales
    """
    return participante.get('hp_actual')

def get_hp_inicial_participante(participante: dict) -> int:
    """
    Obtiene los puntos de vida iniciales de un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        int: Puntos de vida iniciales
    """
    return participante.get('hp_inicial')

def get_attack_participante(participante: dict) -> int:
    """
    Obtiene los puntos de ataque de un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        int: Puntos de ataque
    """
    return participante.get('attack')

def get_defense_participante(participante: dict) -> int:
    """
    Obtiene los puntos de defensa de un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        int: Puntos de defensa
    """
    return participante.get('defense')

def get_nombre_participante(participante: dict) -> str:
    """
    Obtiene el nombre de un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        str: Nombre del participante
    """
    return participante.get('nombre')

def get_cartas_iniciales_participante(participante: dict) -> list[dict]:
    """
    Obtiene las cartas asignadas inicialmente a un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        list: Lista de cartas asignadas al inicio del juego
    """
    return participante.get('mazo_asignado')

def get_cartas_restantes_participante(participante: dict) -> list[dict]:
    """
    Obtiene las cartas que aun no han sido jugadas por un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        list: Lista de cartas disponibles para jugar
    """
    return participante.get('cartas_mazo')

def get_cartas_jugadas_participante(participante: dict) -> list[dict]:
    """
    Obtiene las cartas que ya fueron jugadas por un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        list: Lista de cartas ya utilizadas
    """
    return participante.get('cartas_mazo_usadas')

def get_coordenadas_mazo_inicial(participante: dict):
    """
    Obtiene las coordenadas donde se dibuja el mazo inicial del participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        tuple: Coordenadas (x, y) del mazo inicial
    """
    return participante.get('pos_deck_inicial')

def get_coordenadas_mazo_jugada(participante: dict):
    """
    Obtiene las coordenadas donde se dibuja el mazo de cartas jugadas.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        tuple: Coordenadas (x, y) del mazo de cartas jugadas
    """
    return participante.get('pos_deck_jugados')

def get_carta_actual_participante(participante: dict):
    """
    Obtiene la ultima carta jugada por un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        dict: Ultima carta jugada
    """
    return participante.get('cartas_mazo_usadas')[-1]

def set_nombre_participante(participante: dict, nuevo_nombre: str):
    """
    Asigna un nuevo nombre a un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        nuevo_nombre: Nuevo nombre a asignar
        
    Returns:
        None: Modifica el nombre directamente
    """
    participante['nombre'] = nuevo_nombre

def set_hp_participante(participante: dict, hp_actual: int):
    """
    Asigna un nuevo valor de puntos de vida a un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        hp_actual: Nuevo valor de puntos de vida
        
    Returns:
        None: Modifica los HP directamente
    """
    participante['hp_actual'] = hp_actual

def setear_stat_participante(participante: dict, stat: str, valor: int):
    """
    Asigna un valor especifico a cualquier estadistica de un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        stat: Nombre de la estadistica a modificar
        valor: Nuevo valor a asignar
        
    Returns:
        None: Modifica la estadistica directamente
    """
    participante[stat] = valor

def set_cartas_participante(participante: dict, lista_cartas: list[dict]):
    """
    Asigna un mazo de cartas a un participante y configura sus coordenadas iniciales.
    
    Args:
        participante: Diccionario con los datos del participante
        lista_cartas: Lista de cartas a asignar al participante
        
    Returns:
        None: Modifica las cartas del participante directamente
    """

    for carta_b in lista_cartas:
        carta_b['coordenadas'] = get_coordenadas_mazo_inicial(participante)

    participante['mazo_asignado'] = lista_cartas
    participante['cartas_mazo'] = lista_cartas.copy()

def set_score_participante(participante: dict, score: int):
    """
    Asigna un valor de puntaje a un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        score: Nuevo valor de puntaje
        
    Returns:
        None: Modifica el puntaje directamente
    """
    participante['score'] = score

def get_score_participante(participante: dict) -> int:
    """
    Obtiene el puntaje actual de un participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        int: Puntaje actual
    """
    return participante.get('score')

def add_score_participante(participante: dict, score: int):
    """
    Incrementa el puntaje de un participante sumando puntos adicionales.
    
    Args:
        participante: Diccionario con los datos del participante
        score: Cantidad de puntos a sumar
        
    Returns:
        None: Modifica el puntaje directamente
    """
    participante['score'] += score

def asignar_stats_iniciales_participante(participante: dict):
    """
    Calcula y asigna los stats iniciales de un participante sumando los valores de sus cartas.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        None: Modifica los stats del participante directamente
    """
    participante['hp_inicial'] = aux.reducir(
        carta.get_hp_carta,
        participante.get('mazo_asignado')
    )

    participante['hp_actual'] = participante['hp_inicial']
    
    participante['attack'] = aux.reducir(
        carta.get_atk_carta,
        participante.get('mazo_asignado')
    )

    participante['defense'] = aux.reducir(
        carta.get_def_carta,
        participante.get('mazo_asignado')
    )

def chequear_valor_negativo(stat: int):
    """
    Verifica si un valor es negativo y retorna cero en ese caso.
    
    Args:
        stat: Valor numerico a verificar
        
    Returns:
        int: Cero si el valor es negativo, caso contrario retorna el valor original
    """
    if stat < 0:
        return 0
    return stat

def restar_stats_participante(participante: dict, carta_g: dict, is_critic: bool):
    """
    Calcula y aplica el danio recibido por un participante comparando el ataque del enemigo con su defensa.
    
    Args:
        participante: Diccionario con los datos del participante que recibe danio
        carta_g: Carta del atacante
        is_critic: Indica si el golpe es critico para multiplicar el danio
        
    Returns:
        None: Modifica los stats del participante directamente
    """
    damage_mul = 1
    if is_critic:
        damage_mul = var.CRITICAL_DAMAGE_MULTIPLIER
    carta_jugador = participante.get('cartas_mazo_usadas')[-1]
    
    # Aplicar bonus de estrellas al danio
    atk_base = carta.get_atk_carta(carta_g)
    def_base = carta.get_def_carta(carta_jugador)
    
    atk_con_bonus = carta.calcular_bonus_estrellas(carta_g, atk_base)
    def_con_bonus = carta.calcular_bonus_estrellas(carta_jugador, def_base)
    
    damage = atk_con_bonus - def_con_bonus
    
    print(f'[DANIO] ATK atacante: {atk_base} -> {atk_con_bonus} | DEF defensor: {def_base} -> {def_con_bonus} | Danio base: {damage}')
    
    damage *= damage_mul
    
    if is_critic:
        print(f'[DANIO] Danio final con critico x{damage_mul}: {damage}')
    else:
        print(f'[DANIO] Danio final: {damage}')

    participante['hp_actual'] = chequear_valor_negativo(participante['hp_actual'] - damage)
    participante['attack'] -= carta.get_atk_carta(carta_jugador)
    participante['defense'] -= carta.get_def_carta(carta_jugador)


def jugar_carta(participante: dict):
    """
    Mueve una carta del mazo disponible al mazo de cartas jugadas y la hace visible.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        None: Modifica los mazos del participante directamente
    """
    if participante.get('cartas_mazo'):
        carta_actual = participante.get('cartas_mazo').pop()
        carta.cambiar_visibilidad(carta_actual)
        carta.asignar_coordenadas_carta(carta_actual, get_coordenadas_mazo_jugada(participante))
        participante.get('cartas_mazo_usadas').append(carta_actual)

def reiniciar_datos_participante(player: dict):
    """
    Reinicia todos los datos de un participante a sus valores por defecto.
    
    Args:
        player: Diccionario con los datos del participante
        
    Returns:
        None: Modifica los datos del participante directamente
    """
    set_score_participante(player, 0)
    set_cartas_participante(player, list())
    player['cartas_mazo_usadas'].clear()
    setear_stat_participante(player, 'hp_inicial', 0)
    setear_stat_participante(player, 'hp_actual', 0)
    setear_stat_participante(player, 'ataque', 0)
    setear_stat_participante(player, 'defensa', 0)



def info_to_csv(participante: dict) -> str:
    """
    Genera una cadena de texto en formato CSV con el nombre y puntaje del participante.
    
    Args:
        participante: Diccionario con los datos del participante
        
    Returns:
        str: Linea de texto en formato CSV con nombre y puntaje
    """
    return f'{get_nombre_participante(participante)},{participante.get("score")}\n'

def draw_participante(participante: dict, screen: pg.Surface, mouse_pos=None):
    """
    Dibuja las cartas del participante en la pantalla.
    
    Args:
        participante: Diccionario con los datos del participante
        screen: Superficie de Pygame donde se dibujaran las cartas
        mouse_pos: Posicion del mouse para detectar hover (opcional)
        
    Returns:
        None: Dibuja las cartas en la pantalla
    """

    if participante.get('cartas_mazo'):
        carta.draw_carta(participante.get('cartas_mazo')[-1], screen)
    if participante.get('cartas_mazo_usadas'):
        # Solo zoom en carta jugada
        carta.draw_carta(participante.get('cartas_mazo_usadas')[-1], screen, mouse_pos)


