"""
Modulo controlador de formularios, gestiona la creacion, actualizacion y transicion entre formularios.
"""

import pygame as pg
import modules.forms.menu_form as menu_form
import modules.forms.ranking_form as ranking_form
import modules.forms.form_options as options_form
import modules.variables as var
import modules.forms.base_form as base_form
import modules.forms.form_pause as pause_form
import modules.forms.form_stage as stage_form
import modules.forms.form_name as form_name
import modules.forms.form_wish as wish_form

def create_form_controller(screen: pg.Surface, datos_juego: dict):
    """
    Crea el controlador de formularios con los formularios necesarios.
    
    Args:
        screen: Superficie de Pygame donde se dibujaran los formularios
        datos_juego: Diccionario con los datos iniciales del juego
        
    Returns:
        dict: Controlador de formularios inicializado con todos los formularios del juego
    """

    controller = {} # Diccionario para almacenar el estado del controlador de formularios

    controller['main_screen'] = screen # Pantalla principal del juego
    controller['current_stage'] = 1 
    controller['game_started'] = False 
    controller['player'] = datos_juego.get('player', None) 
    controller['music_config'] = datos_juego.get('music_config', {
        'music_on': True,
        'volume': var.VOLUMEN_INICIAL
    })


    controller['forms_list'] = [
        menu_form.create_form_menu({
            'name': var.FORM_NAMES['MENU'],
            'screen': controller.get('main_screen'),
            'active': True,
            'coord': (0, 0),
            'music_path': var.MUSICA_MENU,
            'background': var.FONDO_MENU,
            'screen_dimensions': var.DIMENSION_PANTALLA,
            'music_config': controller.get('music_config') 
        }),
        ranking_form.create_form_ranking({
            'name': var.FORM_NAMES['RANKING'],
            'screen': controller.get('main_screen'),
            'active': False,
            'coord': (0, 0),
            'music_path': var.MUSICA_RANKING,
            'background': var.FONDO_RANKING,
            'screen_dimensions': var.DIMENSION_PANTALLA,
            'music_config': controller.get('music_config')
        }),
        options_form.create_form_options(
        {
            "name": var.FORM_NAMES['OPTIONS'],
            "screen": controller.get('main_screen'),
            "active": False,
            "coord": (0, 0),
            "music_path": var.MUSICA_OPTIONS,
            "background": var.FONDO_OPTIONS,
            "screen_dimensions": var.DIMENSION_PANTALLA,
            "music_config": controller.get('music_config')
        }),

        pause_form.create_form_pause({    
            "name": var.FORM_NAMES['PAUSE'],
            "screen": controller.get('main_screen'),
            "active": False,
            "coord": (0, 0),
            "music_path": var.MUSICA_PAUSE,
            "background": var.FONDO_PAUSE,
            "screen_dimensions": var.DIMENSION_PANTALLA,
            "music_config": controller.get('music_config')
        }),

        stage_form.crear_form_stage({
            "name": var.FORM_NAMES['STAGE'],
            "screen": controller.get('main_screen'),
            "active": False,
            "coord": (0, 0),
            "music_path": var.MUSICA_STAGE,
            "background": var.FONDO_STAGE,
            "screen_dimensions": var.DIMENSION_PANTALLA,
            "music_config": controller.get('music_config'),
            "jugador": controller.get('player')
        }),
        form_name.create_form_name({
            "name": var.FORM_NAMES['NAME'],
            "screen": controller.get('main_screen'),
            "active": False,
            "coord": (0, 0),
            "music_path": var.MUSICA_RANKING,
            "background": var.FONDO_NAME,
            "screen_dimensions": var.DIMENSION_PANTALLA,
            "music_config": controller.get('music_config'),
            "jugador": controller.get('player')
        }),

        wish_form.create_form_wish({
            "name": var.FORM_NAMES['WISH'],
            "screen": controller.get('main_screen'),
            "active": False,
            "coord": (0, 0),
            "music_path": var.MUSICA_RANKING,
            "background": var.FONDO_WISH,
            "screen_dimensions": var.DIMENSION_PANTALLA,
            "music_config": controller.get('music_config'),
            "jugador": controller.get('player')
        })

    ]

    # INICIAR MUSICA AUTOMATICAMENTE del formulario activo
    for form in controller['forms_list']:
        if form.get('active'):
            base_form.music_on(form)
            break


    return controller

def forms_update(form_controller: dict, eventos: list):
    """
    Actualiza y dibuja el formulario activo junto con el cursor personalizado.
    
    Args:
        form_controller: Diccionario con el controlador de formularios
        eventos: Lista de eventos de Pygame
        
    Returns:
        None: Actualiza y dibuja el formulario activo
    """

    lista_formularios = form_controller.get('forms_list')
    for form in lista_formularios:
        if form.get('active'):
            if form.get('name') == var.FORM_NAMES['MENU']:
                form_menu = lista_formularios[0]
                menu_form.update(form_menu, eventos)
                menu_form.draw(form_menu)
            elif form.get('name') == var.FORM_NAMES['RANKING']:
                form_ranking = lista_formularios[1]
                ranking_form.update(form_ranking, eventos)
                ranking_form.draw(form_ranking)
            elif form.get('name') == var.FORM_NAMES['OPTIONS']:
                form_options = lista_formularios[2] 
                options_form.update(form_options, eventos)
                options_form.draw(form_options)
            elif form.get('name') == var.FORM_NAMES['PAUSE']:
                form_pause = lista_formularios[3]
                pause_form.update(form_pause, eventos)
                pause_form.draw(form_pause)
            elif form.get('name') == var.FORM_NAMES['STAGE']:
                form_stage = lista_formularios[4]
                stage_form.update(form_stage, eventos)
                stage_form.draw(form_stage)
            elif form.get('name') == var.FORM_NAMES['NAME']:
                name_form = lista_formularios[5]
                form_name.update(name_form, eventos)
                form_name.draw(name_form)
            elif form.get('name') == var.FORM_NAMES['WISH']:
                form_wish = lista_formularios[6]
                wish_form.update(form_wish, eventos)
                wish_form.draw(form_wish)
            
            # Dibujar cursor al final, encima de todo
            base_form.draw_cursor(form.get('screen'))

def update(form_controller: dict, eventos: list):
    """
    Procesa los eventos y actualiza el estado del controlador de formularios.
    
    Args:
        form_controller: Diccionario con el controlador de formularios
        eventos: Lista de eventos de Pygame
        
    Returns:
        None
    """
    forms_update(form_controller, eventos)