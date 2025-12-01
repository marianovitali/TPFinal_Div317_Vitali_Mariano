"""
Formulario de deseos especiales durante el juego.
Permite al jugador seleccionar bonus de curacion (HEAL) o escudo protector (SHIELD).
"""

import pygame as pg
import sys
import modules.forms.base_form as base_form
from utn_fra.pygame_widgets import (
    Label, Button, ButtonImage, ImageLabel
)
import modules.variables as var
import modules.forms.form_stage as form_stage
import modules.particip_juego as particip_juego
import modules.stage as stage_juego
def create_form_wish(dict_form_data: dict) -> dict:
    """
    Crea el formulario de deseos para seleccionar bonus especiales durante el juego.
    
    Args:
        dict_form_data: Diccionario con los datos de configuracion del formulario
        
    Returns:
        dict: Formulario de deseos inicializado con todos sus widgets
    """
    
    form = base_form.create_base_form(dict_form_data)

    form['jugador'] = dict_form_data.get('jugador')
    form['wish_type'] = None

    form['lbl_titulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=700,
        text='ELIGE UN DESEO', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70
    )

    form['btn_wish'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2 - 200, y=500,
        text='', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=60,
        on_click=init_wish, on_click_param=form
    )

    form['btn_cancel'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2 + 200, y=500,
        text='CANCEL', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=60,
        on_click=click_resume, on_click_param='form_stage'
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('btn_wish'),
        form.get('btn_cancel')
    ]

    var.dict_forms_status[form.get('name')] = form

    return form


def update_wish_type(dict_form_data: dict, wish_type: str):
    """
    Actualiza el tipo de deseo seleccionado y modifica el texto del boton correspondiente.
    
    Args:
        dict_form_data: Diccionario con los datos del formulario
        wish_type: Tipo de deseo (HEAL o SHIELD)
        
    Returns:
        None
    """
    dict_form_data['wish_type'] = wish_type
    dict_form_data.get('widgets_list')[1].update_text(f'WISH: {wish_type}', pg.Color('yellow'))


def click_resume(form_name: str):
    """
    Vuelve al formulario especificado sin aplicar ningun deseo.
    
    Args:
        form_name: Nombre del formulario al que volver
        
    Returns:
        None
    """
    base_form.cambiar_pantalla(form_name)

def init_wish(form_dict_data: dict):
    """
    Aplica el deseo seleccionado (HEAL recupera HP o SHIELD activa escudo protector) y regresa al juego.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    wish_type = form_dict_data.get('wish_type')
    jugador = form_dict_data.get('jugador')

    stage_form = var.dict_forms_status.get('form_stage')
    stage = stage_form.get('stage')

    if wish_type == 'HEAL':
        wish = 'heal'
    else:
        wish = 'shield'
    stage_juego.modificar_estado_bonus(stage, wish)


    if wish_type == 'SHIELD':
        # Activar el shield en el stage_data
        stage['shield_activo'] = True
        print('SHIELD activado! Se reflejara el proximo danio recibido')
    
    else: #HEAL
        hp_inicial = particip_juego.get_hp_inicial_participante(jugador)
        hp_actual = particip_juego.get_hp_participante(jugador)
        hp_perdida = hp_inicial - hp_actual

        hp_bonus = int(hp_perdida * 0.75)

        nuevo_hp = hp_actual + hp_bonus
        print(f'Anterior HP: {hp_actual}, Nuevo HP: {nuevo_hp}')
        particip_juego.set_hp_participante(jugador, nuevo_hp)

    click_resume('form_stage')

def update(form_dict_data: dict, eventos: list):
    """
    Actualiza el estado del formulario de deseos.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        eventos: Lista de eventos de Pygame
        
    Returns:
        None
    """
    base_form.update(form_dict_data)

def draw(form_dict_data: dict):
    """
    Dibuja el formulario de deseos con todos sus widgets.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)