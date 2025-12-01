"""
Modulo para manejo de cartas del juego.
Provee funciones para inicializar, visualizar y obtener estadisticas de las cartas.
"""

import modules.auxiliar as aux
import modules.variables as var
import pygame as pg

def inicializar_carta(dict_card: dict, coords: list[int]) -> dict:
    """
    Inicializa una carta con sus propiedades visuales y de estado.
    
    Args:
        dict_card: Diccionario con los datos base de la carta
        coords: Coordenadas iniciales (x, y) de la carta en pantalla
        
    Returns:
        dict: Carta inicializada con todas sus propiedades
    """
    card = dict_card
    card['visible'] = False
    card['coordenadas'] = coords

    card['imagen'] = None
    card['rect'] = None

    return card

def esta_visible(dict_card: dict) -> bool:
    """
    Verifica si una carta esta visible mostrando su frente.
    
    Args:
        dict_card: Diccionario con los datos de la carta
        
    Returns:
        bool: True si la carta esta visible, False si esta oculta
    """
    return dict_card.get('visible', False)

def cambiar_visibilidad(dict_card: dict):
    """
    Alterna el estado de visibilidad de una carta entre visible y oculta.
    
    Args:
        dict_card: Diccionario con los datos de la carta
        
    Returns:
        None: Modifica el estado de visibilidad de la carta directamente
    """
    dict_card['visible'] = not dict_card.get('visible')

def get_hp_carta(dict_card: dict) -> int:
    """
    Obtiene los puntos de vida de una carta.
    
    Args:
        dict_card: Diccionario con los datos de la carta
        
    Returns:
        int: Puntos de vida de la carta
    """
    return dict_card.get('hp')


def get_def_carta(dict_card: dict) -> int:
    """
    Obtiene los puntos de defensa de una carta.
    
    Args:
        dict_card: Diccionario con los datos de la carta
        
    Returns:
        int: Puntos de defensa de la carta
    """
    return dict_card.get('def')
def get_atk_carta(dict_card: dict) -> int:
    """
    Obtiene los puntos de ataque de una carta.
    
    Args:
        dict_card: Diccionario con los datos de la carta
        
    Returns:
        int: Puntos de ataque de la carta
    """
    return dict_card.get('atk')
def get_estrellas_carta(dict_card: dict) -> int:
    """
    Obtiene la cantidad de estrellas de una carta.
    
    Args:
        dict_card: Diccionario con los datos de la carta
        
    Returns:
        int: Numero de estrellas de la carta
    """
    return dict_card.get('estrellas', 0)

def calcular_bonus_estrellas(dict_card: dict, stat_base: int) -> int:
    """
    Calcula el bonus de estrellas aplicado a una estadistica base donde cada estrella suma 1% adicional.
    
    Args:
        dict_card: Diccionario con los datos de la carta
        stat_base: Valor base de la estadistica a potenciar
        
    Returns:
        int: Valor de la estadistica con el bonus aplicado
    """
    estrellas = get_estrellas_carta(dict_card)
    bonus_porcentaje = estrellas / 100
    stat_con_bonus = int(stat_base * (1 + bonus_porcentaje))
    return stat_con_bonus


def asignar_coordenadas_carta(dict_card: dict, coordenadas: tuple[int]):
    """
    Asigna nuevas coordenadas a una carta en pantalla.
    
    Args:
        dict_card: Diccionario con los datos de la carta
        coordenadas: Tupla con las nuevas coordenadas (x, y)
        
    Returns:
        None: Modifica las coordenadas de la carta directamente
    """
    dict_card['coordenadas'] = coordenadas
    


def draw_carta(dict_card: dict, screen: pg.Surface, mouse_pos=None):
    """
    Dibuja una carta en pantalla con efecto de zoom al pasar el mouse.
    
    Args:
        dict_card: Diccionario con los datos de la carta
        screen: Superficie de Pygame donde se dibujara la carta
        mouse_pos: Posicion del mouse para detectar hover (opcional)
        
    Returns:
        None: Dibuja la carta en la pantalla
    """
    # Determinar si hay hover (colision con mouse)
    is_hovering = False
    if mouse_pos and dict_card.get('rect'):
        is_hovering = dict_card['rect'].collidepoint(mouse_pos)
    
    # Tamanio base con zoom al pasar mouse
    if is_hovering:
        carta_size = var.CARTA_SIZE_HOVER
    else:
        carta_size = var.CARTA_SIZE_NORMAL
    
    if dict_card.get('visible'):
        dict_card['imagen'] = aux.redimesionar_imagen(dict_card.get('ruta_frente'), carta_size)
    else:
        dict_card['imagen'] = aux.redimesionar_imagen(dict_card.get('ruta_reverso'), carta_size)

    dict_card['rect'] = dict_card['imagen'].get_rect()
    
    # Mantener el centro al hacer zoom para que no salte
    if is_hovering and dict_card.get('coordenadas'):
        dict_card['rect'].center = (
            dict_card.get('coordenadas')[0] + 100,
            dict_card.get('coordenadas')[1] + 150
        )
    else:
        dict_card['rect'].topleft = dict_card.get('coordenadas')

    screen.blit(dict_card['imagen'], dict_card['rect'])