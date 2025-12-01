"""
Formulario del menu principal del juego.
Ofrece opciones para iniciar partida, ver ranking, configurar opciones o salir del juego.
"""

import pygame as pg
import sys
import modules.forms.base_form as base_form
from utn_fra.pygame_widgets import (
    Label, Button, ButtonImage, ImageLabel
)
import modules.variables as var
import modules.forms.form_stage as form_stage

def create_form_menu(dict_form_data: dict) -> dict:
    """
    Crea el formulario del menu principal con opciones para jugar, ver ranking y configurar.
    
    Args:
        dict_form_data: Diccionario con los datos de configuracion del formulario
        
    Returns:
        dict: Formulario de menu principal inicializado con todos sus widgets
    """
    
    form = base_form.create_base_form(dict_form_data)

    # form['lbl_titulo'] = Label(
    #     x= 1200, y=320,
    #     text='Menu principal', screen=form.get('screen'),
    #     font_path=var.FONT_AKSARAKOMIK, font_size=75, color=pg.Color('orange')
    # )

    form['lbl_titulo2'] = ButtonImage(
        x= 1200, y=320, text='Dragon Ball Z TCG',
        image_path=var.IMG_MENU, screen=form.get('screen'),
        width=552, height=104
    )

    form['btn_play'] = Button(
    x= 1200, y=450,
    text='JUGAR', screen=form.get('screen'),
    font_path=var.FONT_AKSARAKOMIK, font_size=70, color=pg.Color('orange'),
    on_click=iniciar_stage, on_click_param=var.FORM_NAMES['STAGE']
    )

    form['btn_ranking'] = Button(
    x= 1200, y=530,
    text='RANKING', screen=form.get('screen'),
    font_path=var.FONT_AKSARAKOMIK, font_size=70, color=pg.Color('orange'),
    on_click=base_form.cambiar_pantalla, on_click_param=var.FORM_NAMES['RANKING']
    )
    form['btn_options'] = Button(
    x= 1200, y=610,
    text='OPCIONES', screen=form.get('screen'),
    font_path=var.FONT_AKSARAKOMIK, font_size=70, color=pg.Color('orange'),
    on_click=base_form.cambiar_pantalla, on_click_param=var.FORM_NAMES['OPTIONS']
    )

    form['btn_exit'] = Button(
        x= 1200, y=690,
        text='SALIR', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70, color=pg.Color('orange'),
        on_click=salir_juego, on_click_param=None
    )

    # form['btn_exit2'] = ButtonImage(
    #     x=1200, y=750, text='Salir',
    #     image_path=var.IMG_EXIT, screen=form.get('screen'),
    #     on_click=salir_juego, on_click_param=None, width=150, height=75
    # )

    form['widgets_list'] = [
        # form.get('lbl_titulo'),
        form.get('lbl_titulo2'),
        form.get('btn_play'),
        form.get('btn_ranking'),
        form.get('btn_options'),
        form.get('btn_exit')
    ]

    var.dict_forms_status[form.get('name')] = form
    return form

def iniciar_stage(form_name: str,):
    """
    Cambia al formulario de stage e inicia una nueva partida.
    
    Args:
        form_name: Nombre del formulario stage
        
    Returns:
        None
    """
    base_form.cambiar_pantalla(form_name)
    stage_form = var.dict_forms_status.get(form_name)
    form_stage.iniciar_nueva_partida(stage_form)


def salir_juego(_):
    """
    Cierra el juego terminando Pygame y finalizando el programa.
    
    Args:
        _: Parametro no utilizado
        
    Returns:
        None
    """
    pg.quit()
    exit()

def draw(dict_form_data: dict):
    """
    Dibuja el formulario del menu principal con todos sus widgets.
    
    Args:
        dict_form_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    base_form.draw(dict_form_data)
    base_form.draw_widgets(dict_form_data)

# def events_handler():
#     events = pg.event.get()

#     for event in events:
#         if event.type == pg.MOUSEBUTTONDOWN:
#             x, y = event.pos
#             print(f'Coordinadas del clic: {x}, {y}')
#         if event.type == pg.QUIT:
#             salir_juego()

def update(dict_form_data: dict, eventos: list):
    """
    Actualiza el estado del formulario del menu principal.
    
    Args:
        dict_form_data: Diccionario con los datos del formulario
        eventos: Lista de eventos de Pygame
        
    Returns:
        None
    """
    # events_handler()
    base_form.update(dict_form_data)

