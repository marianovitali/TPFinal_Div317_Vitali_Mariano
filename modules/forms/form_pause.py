"""
Formulario de pausa del juego.
Ofrece opciones para reanudar, reiniciar el nivel o volver al menu principal.
"""

import pygame as pg
import sys
import modules.forms.base_form as base_form
from utn_fra.pygame_widgets import (
    Label, Button, ButtonImage, ImageLabel
)
import modules.variables as var
import modules.forms.form_stage as form_stage


def create_form_pause(dict_form_data: dict) -> dict:
    """
    Crea el formulario de pausa con opciones para reanudar, reiniciar o salir al menu.
    
    Args:
        dict_form_data: Diccionario con los datos de configuracion del formulario
        
    Returns:
        dict: Formulario de pausa inicializado con todos sus widgets
    """

    form = base_form.create_base_form(dict_form_data)
    form['previous_volume'] = None

    form['btn_resume'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=500,
        text='RESUME', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70, color=pg.Color('orange'),
        on_click=base_form.salir_de_pause, on_click_param=var.FORM_NAMES['STAGE']
    )

    form['btn_restart'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=580,
        text='RESTART', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70, color=pg.Color('orange'),
        on_click=restart_stage, on_click_param={'form_name': var.FORM_NAMES['STAGE']}
    )
    form['btn_menu'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=660,
        text='MAIN MENU', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70, color=pg.Color('orange'),
        on_click=base_form.salir_de_pause, on_click_param=var.FORM_NAMES['MENU']
    )

    form['widgets_list'] = [
        form.get('btn_resume'),
        form.get('btn_restart'),
        form.get('btn_menu')
    ]
    var.dict_forms_status[form.get('name')] = form

    return form

def restart_stage(params: dict):
    """
    Reinicia el nivel actual desde el menu de pausa.
    
    Args:
        params: Diccionario con el nombre del formulario stage
        
    Returns:
        None
    """
    stage_form = var.dict_forms_status.get(params.get('form_name'))
    base_form.salir_de_pause(params.get('form_name'))
    form_stage.iniciar_nueva_partida(stage_form)


def draw(form_dict_data: dict):
    """
    Dibuja el formulario de pausa con todos sus widgets.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)

def update(form_dict_data: dict, eventos: list):
    """
    Actualiza el estado del formulario de pausa.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        eventos: Lista de eventos de Pygame
        
    Returns:
        None
    """
    base_form.update(form_dict_data)