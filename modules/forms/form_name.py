"""
Formulario para ingreso del nombre del jugador al finalizar una partida.
Muestra el puntaje obtenido y permite guardar el resultado en el ranking.
"""

import pygame as pg
import modules.forms.base_form as base_form
from utn_fra.pygame_widgets import (
    Label, Button, TextBox
)
import modules.variables as var
import modules.forms.form_stage as form_stage
import modules.particip_juego as particip_juego
import modules.auxiliar as aux
import modules.sonido as sonido

def create_form_name(dict_form_data: dict) -> dict:
    """
    Crea el formulario para ingresar nombre del jugador al finalizar la partida.
    
    Args:
        dict_form_data: Diccionario con los datos de configuracion del formulario
        
    Returns:
        dict: Formulario de nombre inicializado con todos sus widgets
    """
    form = base_form.create_base_form(dict_form_data)
    form['jugador'] = dict_form_data.get('jugador')
    form['info_submitida'] = False
    form['limit_char'] = var.MAX_NAME_LENGTH

    form['lbl_subtitulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=350,
        text='', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=50, color=pg.Color('orange')
    )

    form['lbl_score'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2 - 20 , y=280,
        text=f"{particip_juego.get_score_participante(form.get('jugador'))}",
        font_path=var.FONT_AKSARAKOMIK, font_size=50,
        color=pg.Color('orange'), screen=form.get('screen')
    )

    form['lbl_nombre_texto'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=450,
        text="",
        font_path=var.FONT_AKSARAKOMIK, font_size=50,
        color=pg.Color('orange'), screen=form.get('screen')
    )

    form['text_box'] = TextBox(
        x= var.DIMENSION_PANTALLA[0] // 2, y=460,
        text=f"_________",
        font_path=var.FONT_AKSARAKOMIK, font_size=50,
        color=pg.Color('orange'), screen=form.get('screen')
    )

    form['btn_submit'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2, y=530,
        text='CONFIRMAR NOMBRE', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=40, color=pg.Color('black'),
        on_click=submit_name, on_click_param=form
    )

    form['btn_submit2'] = Button(
        x= var.DIMENSION_PANTALLA[0] // 2 + 2, y=532,
        text='CONFIRMAR NOMBRE', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=40, color=pg.Color('orange'),
        on_click=submit_name, on_click_param=form
    )

    form['widgets_list'] = [
        form.get('lbl_subtitulo'),
        form.get('lbl_score'),
        form.get('lbl_nombre_texto'),
        form.get('btn_submit'),
        form.get('btn_submit2')
    ]

    var.dict_forms_status[form.get('name')] = form
    return form

def clear_text(form_data: dict):
    """
    Limpia el texto ingresado en el campo de entrada.
    
    Args:
        form_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    form_data.get('text_box').writing = ''

def update_texto_victoria(form_dict_data: dict, win_status: bool):
    """
    Actualiza el formulario segun si el jugador gano o perdio cambiando fondo y musica.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        win_status: True si el jugador gano, False si perdio
        
    Returns:
        None
    """
    if win_status:
        form_dict_data.get('lbl_subtitulo').update_text(text='HAS GANADO!! ERES EL CAMPEON', color=pg.Color('orange'))
        form_dict_data['surface'] = pg.image.load(var.FONDO_VICTORY).convert_alpha()
        form_dict_data['surface'] = pg.transform.scale(form_dict_data['surface'], var.DIMENSION_PANTALLA)
        form_dict_data['music_path'] = var.MUSICA_VICTORY
        form_dict_data['music_config'] = {'loops': 0}  
        base_form.music_on(form_dict_data)
    else:
        form_dict_data.get('lbl_subtitulo').update_text(text='HAS PERDIDO. INTENTA DE NUEVO.', color=pg.Color('orange'))
        form_dict_data['surface'] = pg.image.load(var.FONDO_DEFEAT).convert_alpha()
        form_dict_data['surface'] = pg.transform.scale(form_dict_data['surface'], var.DIMENSION_PANTALLA)
        form_dict_data['music_path'] = var.MUSICA_DEFEAT
        form_dict_data['music_config'] = {'loops': 0}  
        base_form.music_on(form_dict_data)


def submit_name(form_data: dict):
    """
    Guarda el nombre y puntaje del jugador en el archivo CSV y cambia al ranking.
    
    Args:
        form_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    nombre_jugador = form_data.get('lbl_nombre_texto').text

    particip_juego.set_nombre_participante(form_data.get('jugador'), nombre_jugador)

    nombre_jugador_seteado = particip_juego.get_nombre_participante(form_data.get('jugador'))
    puntaje_jugador = particip_juego.get_score_participante(form_data.get('jugador'))

    print(f'Nombre del jugador: {nombre_jugador_seteado}, Puntaje: {puntaje_jugador}')
    data_to_csv = particip_juego.info_to_csv(form_data.get('jugador'))

    aux.guardar_info_csv(data_to_csv)
    form_data['info_submitida'] = True

    form_data.get('text_box').writing = ''

    base_form.cambiar_pantalla('form_ranking')

def update(form_dict_data: dict, events_list: list):
    """
    Actualiza el puntaje y el texto ingresado limitando la cantidad de caracteres.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        events_list: Lista de eventos de Pygame
        
    Returns:
        None
    """
    form_dict_data['score'] = particip_juego.get_score_participante(form_dict_data.get('jugador'))

    form_dict_data.get('widgets_list')[1].update_text(text=f'SCORE: {form_dict_data.get("score")}', color=pg.Color('orange'))
    form_dict_data.get('widgets_list')[2].update_text(text=f'{form_dict_data.get("text_box").writing.upper()[:form_dict_data.get("limit_char")]}', color=pg.Color('orange'))

    form_dict_data.get('text_box').writing = form_dict_data.get('text_box').writing.upper()[:form_dict_data.get('limit_char')]
    form_dict_data.get('text_box').update(events_list)
    base_form.update(form_dict_data)

def draw(form_dict_data: dict):
    """
    Dibuja el formulario con todos sus widgets y el campo de texto.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)
    form_dict_data.get('text_box').draw()
