"""
Formulario para visualizacion del ranking de mejores puntajes.
Carga y muestra los top 8 puntajes guardados en el archivo CSV.
"""

import pygame as pg
import sys
import modules.forms.base_form as base_form
import modules.auxiliar as aux


from utn_fra.pygame_widgets import (
    Label, Button
)
import modules.variables as var


def create_form_ranking(dict_form_data: dict) -> dict:
    """
    Crea el formulario de ranking para mostrar los mejores puntajes del juego.
    
    Args:
        dict_form_data: Diccionario con los datos de configuracion del formulario
        
    Returns:
        dict: Formulario de ranking inicializado con sus widgets base
    """
    
    form = base_form.create_base_form(dict_form_data)

    form['lista_ranking_file'] = []

    form['lista_ranking_GUI'] = []

    form['data_loaded'] = False  # Indicador para saber si los datos del ranking han sido cargados

    form['lbl_titulo'] = Label(
        x=var.DIMENSION_PANTALLA[0] // 2, y=320,
        text='RANKING', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=70,
        color=pg.Color('orange')
    )

    form['lbl_volver'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2, y=810,
        text='Volver al Menu', screen=form.get('screen'),
        font_path=var.FONT_AKSARAKOMIK, font_size=45,
        color=pg.Color('orange'),
        on_click=cambiar_pantalla, on_click_param=[form, var.FORM_NAMES['MENU']]
    )

    form['widgets_list'] = [
        form.get('lbl_titulo'),
        form.get('lbl_volver')
    ]

    var.dict_forms_status[form.get('name')] = form

    return form

def cambiar_pantalla(param_list: list):
    """
    Cambia de pantalla limpiando los datos del ranking antes de la transicion.
    
    Args:
        param_list: Lista con el formulario de ranking y nombre del formulario destino
        
    Returns:
        None
    """
    form_ranking = param_list[0]
    form_name = param_list[1]
    
    print(f"Cambiando a form: {form_name}")
    
    # Limpiar datos del ranking
    form_ranking['data_loaded'] = False
    form_ranking['lista_ranking_GUI'] = []
    form_ranking['lista_ranking_file'] = []
    
    # Usar el NUEVO sistema
    base_form.cambiar_pantalla(form_name)

def inicializar_ranking_archivo(form_dict_data: dict):
    """
    Carga los datos del ranking desde el archivo CSV si aun no fueron cargados.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    if not form_dict_data.get('data_loaded'):
        form_dict_data['lista_ranking_file'] = aux.cargar_ranking(var.RANKING_CSV, top=8)
        init_ranking_data(form_dict_data)
        form_dict_data['data_loaded'] = True


def init_ranking_data(form_dict_data: dict):
    """
    Crea los widgets de etiquetas para mostrar el ranking en pantalla con posicion, nombre y puntaje.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """

    matrix = form_dict_data.get('lista_ranking_file')

    for indice_fila in range(len(matrix)):
        fila = matrix[indice_fila]

        y_coord_inicial = 400 + indice_fila * 50

        posicion = Label(
            x=var.DIMENSION_PANTALLA[0] // 2 - 200, y=y_coord_inicial,
            text=f"{indice_fila + 1}.", screen=form_dict_data.get('screen'),
            font_path=var.FONT_AKSARAKOMIK, font_size=50,
            color=pg.Color('orange')
        )

        nombre = Label(
            x=var.DIMENSION_PANTALLA[0] // 2, y=y_coord_inicial,
            text=str(fila[0]), screen=form_dict_data.get('screen'),
            font_path=var.FONT_AKSARAKOMIK, font_size=50,
            color=pg.Color('orange')
        )

        score = Label(
            x=var.DIMENSION_PANTALLA[0] // 2 + 200, y=y_coord_inicial,
            text=str(fila[1]), screen=form_dict_data.get('screen'),
            font_path=var.FONT_AKSARAKOMIK, font_size=50,
            color=pg.Color('orange')
        )

        form_dict_data['lista_ranking_GUI'].append(posicion)
        form_dict_data['lista_ranking_GUI'].append(nombre)
        form_dict_data['lista_ranking_GUI'].append(score)

def draw(form_dict_data: dict):
    """
    Dibuja el formulario de ranking con todos los widgets y las entradas del ranking.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    base_form.draw(form_dict_data)
    base_form.draw_widgets(form_dict_data)

    for widget in form_dict_data['lista_ranking_GUI']:
        widget.draw()


def update(form_dict_data: dict, eventos: list):
    """
    Actualiza el formulario de ranking cargando los datos si es necesario.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        eventos: Lista de eventos de Pygame
        
    Returns:
        None
    """

    if not form_dict_data['data_loaded']:
        inicializar_ranking_archivo(form_dict_data)


    base_form.update(form_dict_data)