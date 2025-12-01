"""
Formulario de opciones y configuracion del juego.
Permite activar o desactivar musica y ajustar el volumen.
"""

import pygame as pg
import sys
import modules.forms.base_form as base_form
from utn_fra.pygame_widgets import (
    Label, Button
)
import modules.variables as var
import modules.sonido as sonido


def create_form_options(dict_form_data: dict) -> dict:
    """
    Crea el formulario de opciones con controles de musica y volumen.
    
    Args:
        dict_form_data: Diccionario con los datos de configuracion del formulario
        
    Returns:
        dict: Formulario de opciones inicializado con todos sus widgets
    """
    form = base_form.create_base_form(dict_form_data)
    
    form['lbl_titulo'] = Label(
        x=1200, y=350,
        text='OPTIONS', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=75, color=pg.Color('orange')
    )

    form['btn_music_on'] = Button(
        x=1200, y=500,
        text='MUSIC ON', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70,
        on_click=activar_musica, on_click_param=form, color=pg.Color('orange')
    )
    
    form['btn_music_off'] = Button(
        x=1200, y=580,
        text='MUSIC OFF', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70,
        on_click=desactivar_musica, on_click_param=form, color=pg.Color('orange')
    )

    form['btn_vol_down'] = Button(
        x=1100, y=660,
        text='<', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70,
        on_click=modificar_volumen, on_click_param=(-10), color=pg.Color('orange')
    )

    form['btn_vol_up'] = Button(
        x=1300, y=660,
        text='>', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70,
        on_click=modificar_volumen, on_click_param=10, color=pg.Color('orange')
    )

    form['lbl_vol'] = Label(
        x=1200, y=660,
        text=f'{sonido.get_actual_volume()}', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70, color=pg.Color('orange')
    )

    form['btn_volver'] = Button(
        x=1200, y=740,
        text='VOLVER', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70,
        on_click=base_form.cambiar_pantalla, on_click_param=var.FORM_NAMES['MENU'], color=pg.Color('orange')
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('btn_music_on'),
        form.get('btn_music_off'),
        form.get('btn_vol_up'),
        form.get('btn_vol_down'),
        form.get('lbl_vol'),
        form.get('btn_volver')
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def modificar_volumen(volumen: int):
    """
    Ajusta el volumen de la musica sumando o restando el valor especificado.
    
    Args:
        volumen: Incremento o decremento del volumen
        
    Returns:
        None
    """
    vol_actual = sonido.get_actual_volume()
    nuevo_vol = vol_actual + volumen
    # Limitar entre 0 y 100
    nuevo_vol = max(0, min(100, nuevo_vol))
    sonido.set_volume(nuevo_vol)

def activar_musica(form_data):
    """
    Activa la musica del juego y comienza a reproducirla.
    
    Args:
        form_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    sonido.set_music_enabled(True)
    # Forzar reproduccion aunque sea la misma cancion (puede estar detenida)
    sonido.play_music()

def desactivar_musica(_):
    """
    Desactiva la musica del juego con efecto de desvanecimiento.
    
    Args:
        _: Parametro no utilizado
        
    Returns:
        None
    """
    sonido.set_music_enabled(False)

# def cambiar_pantalla(form_name: str):
#     base_form.cambiar_pantalla(form_name)

def draw(form_dict_data: dict):
    """
    Dibuja el formulario de opciones con todos sus widgets.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)

def update(form_dict_data: dict, eventos: list):
    """
    Actualiza el valor del volumen mostrado en la etiqueta correspondiente.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        eventos: Lista de eventos de Pygame
        
    Returns:
        None
    """
    lbl_vol: Label = form_dict_data.get('widgets_list')[5]
    lbl_vol.update_text(text=f'{sonido.get_actual_volume()}', color=pg.Color('red'))
    base_form.update(form_dict_data)