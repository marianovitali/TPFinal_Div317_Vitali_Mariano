"""
Formulario principal del nivel de juego.
Maneja la interfaz de batalla, estadisticas de jugadores, cartas en juego y botones de accion (jugar, heal, shield).
"""

import pygame as pg
import sys
import modules.forms.base_form as base_form
from utn_fra.pygame_widgets import (
    Label, Button, ButtonImage, ImageLabel
)
import modules.forms.form_name as form_name
import modules.variables as var
import modules.stage as stage_juego
import modules.carta as carta_jugador
import modules.particip_juego as particip_juego
import modules.forms.form_wish as form_wish

def crear_form_stage(dict_form_data: dict) -> dict:
    """
    Crea el formulario principal del nivel de juego con todos los elementos de interfaz.
    
    Args:
        dict_form_data: Diccionario con los datos de configuracion del formulario
        
    Returns:
        dict: Formulario de stage inicializado con todos sus widgets y controles
    """

    form = base_form.create_base_form(dict_form_data)

    form['actual_level'] = 1
    form['jugador'] = dict_form_data.get('jugador')

    form['stage'] = stage_juego.inicializar_stage(jugador=form.get('jugador'), pantalla=form.get('screen'), nro_stage=form.get('actual_level'))

    form['lbl_timer'] = Label(
        x=var.DIMENSION_PANTALLA[0] - 150, y=50,
        text=f'Time: {stage_juego.obtener_tiempo(form.get("stage"))}',
        font_path=var.FONT_AKSARAKOMIK, font_size=50,
        align='center', color=var.colores['blanco'], screen=form.get('screen')
    )

    form['lbl_score'] = Label(
        x=150, y=50,
        text=f'Score: 0',
        font_path=var.FONT_AKSARAKOMIK, font_size=50,
        align='center', color=var.colores['blanco'], screen=form.get('screen')
    )


    form['lbl_carta_e'] = Label(
        x=800, y=400,
        text=f'',
        font_path=var.FONT_AKSARAKOMIK, font_size=40,
        align='center', color=pg.Color('cyan'), screen=form.get('screen')
    )

    form['lbl_carta_p'] = Label(
        x=800, y=450,
        text=f'',
        font_path=var.FONT_AKSARAKOMIK, font_size=40,
        align='center', color=var.colores['naranja'], screen=form.get('screen')
    )
    # STATS ENEMIGO
    form['lbl_enemigo_hp'] = Label(
        x=200, y=250,
        text=f'',
        font_path=var.FONT_AKSARAKOMIK, font_size=32,
        align='center', color=var.colores['blanco'], screen=form.get('screen')
    )

    form['lbl_enemigo_atk'] = Label(
        x=200, y=290,
        text=f'',
        font_path=var.FONT_AKSARAKOMIK, font_size=32,
        align='center', color=var.colores['blanco'], screen=form.get('screen')
    )

    form['lbl_enemigo_def'] = Label(
        x=200, y=330,
        text=f'',
        font_path=var.FONT_AKSARAKOMIK, font_size=32,
        align='center', color=var.colores['blanco'], screen=form.get('screen')
    )

    form['lbl_enemigo_cards'] = Label(
        x=200, y=360,
        text=f'Cards: 0',
        font_path=var.FONT_AKSARAKOMIK, font_size=25,
        align='center', color=var.colores['blanco'], screen=form.get('screen')
    )

    # STATS PLAYER
    form['lbl_jugador_hp'] = Label(
        x=200, y=600,
        text=f'',
        font_path=var.FONT_AKSARAKOMIK, font_size=32,
        align='center', color=var.colores['blanco'], screen=form.get('screen')
    )

    form['lbl_jugador_atk'] = Label(
        x=200, y=640,
        text=f'',
        font_path=var.FONT_AKSARAKOMIK, font_size=32,
        align='center', color=var.colores['blanco'], screen=form.get('screen')
    )

    form['lbl_jugador_def'] = Label(
        x=200, y=680,
        text=f'',
        font_path=var.FONT_AKSARAKOMIK, font_size=32,
        align='center', color=var.colores['blanco'], screen=form.get('screen')
    )

    form['lbl_jugador_cards'] = Label(
        x=200, y=710,
        text=f'Cards: 0',
        font_path=var.FONT_AKSARAKOMIK, font_size=25,
        align='center', color=var.colores['blanco'], screen=form.get('screen')
    )
    # ========= BOTONES =========

    form['btn_play'] = ButtonImage(
        x=var.DIMENSION_PANTALLA[0] // 2 + 600, y=var.DIMENSION_PANTALLA[1] - 400,
        text='JUGAR', screen=form.get('screen'), image_path=var.IMG_BTN_PLAY, width=350, height=300,
        on_click=jugar_mano, on_click_param=form
    )

    form['btn_heal'] = ButtonImage(
        x=var.DIMENSION_PANTALLA[0] // 2 + 500, y=var.DIMENSION_PANTALLA[1] - 150,
        text='HEAL', screen=form.get('screen'), image_path=var.IMG_BTN_HEAL, width=250, height=200,
        on_click=call_wish_form, on_click_param={'form': form, 'wish': 'HEAL'}
    )

    form['btn_shield'] = ButtonImage(
    x=var.DIMENSION_PANTALLA[0] // 2 + 700, y=var.DIMENSION_PANTALLA[1] - 150,
    text='SHIELD', screen=form.get('screen'), image_path=var.IMG_BTN_SHIELD, width=250, height=200,
    on_click=call_wish_form, on_click_param={'form': form, 'wish': 'SHIELD'}
    )
        # ========= RADARES =========
    form['img_radar_azul'] = ImageLabel(
        x=10, y=100,
        image_path=var.IMG_RADAR_AZUL, screen=form.get('screen'),
        text='', width=450, height=350, font_path=var.FONT_AKSARAKOMIK, font_size=30, color=pg.Color('orange')
    )

    form['img_radar_naranja'] = ImageLabel(
        x=10, y=450,
        image_path=var.IMG_RADAR_NARANJA, screen=form.get('screen'),
        text='', width=450, height=350, font_path=var.FONT_AKSARAKOMIK, font_size=30, color=pg.Color('orange')
    )

    form['widgets_list'] = [
        form.get('lbl_timer'),
        form.get('lbl_score'),
        form.get('btn_play'),
        form.get('lbl_carta_e'),
        form.get('lbl_carta_p'),
        form.get('img_radar_azul'),
        form.get('img_radar_naranja'),
        form.get('lbl_enemigo_hp'),
        form.get('lbl_enemigo_atk'),
        form.get('lbl_enemigo_def'),
        form.get('lbl_enemigo_cards'),
        form.get('lbl_jugador_hp'),
        form.get('lbl_jugador_atk'),
        form.get('lbl_jugador_def'),
        form.get('lbl_jugador_cards')
    ]

    form['widgets_list_bonus'] = [
        form.get('btn_heal'),
        form.get('btn_shield')
    ]


    var.dict_forms_status[form.get('name')] = form

    return form


def jugar_mano(form_dict_data: dict):
    """
    Ejecuta una jugada donde ambos participantes juegan una carta y se resuelve el combate.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    stage = form_dict_data.get('stage')
    if stage_juego.hay_jugadores_con_cartas(stage):
        critical, ganador_mano = stage_juego.jugar_mano(stage)
        print(f'Ganador de la mano: {ganador_mano}')
        
        # Guardar timestamp si hubo critico
        if critical:
            stage['critical_hit_time'] = pg.time.get_ticks()
            sound_critical = pg.mixer.Sound(var.SOUND_CRITICAL_HIT)
            sound_critical.play()
            
    elif not stage_juego.hay_jugadores_con_cartas(stage) and stage_juego.esta_finalizado(stage):
        ganador = stage_juego.obtener_ganador(stage)
        print(f'El ganador del juego es: {particip_juego.get_nombre_participante(ganador)}')
        
        if particip_juego.get_nombre_participante(ganador) == 'Enemigo':
            win_status = False
        else:
            win_status = True

        name_form = var.dict_forms_status.get('form_name')
        form_name.update_texto_victoria(name_form, win_status)

        base_form.set_active('form_name')

def verificar_terminado(form_dict_data: dict):
    """
    Verifica si el juego termino y cambia al formulario de nombre mostrando victoria o derrota.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    stage = form_dict_data.get('stage')
    if stage_juego.esta_finalizado(stage):
        print('EL JUEGO HA TERMINADO')
        if particip_juego.get_nombre_participante(
            stage_juego.obtener_ganador(stage)
        ) == 'Enemigo':
            win_status = False
        else:
            win_status = True
        name_form = var.dict_forms_status.get('form_name')
        form_name.update_texto_victoria(name_form, win_status)
        base_form.set_active('form_name')

def call_wish_form(params: dict):
    """
    Abre el formulario de deseos especificando el tipo de deseo a usar.
    
    Args:
        params: Diccionario con el formulario y tipo de deseo
        
    Returns:
        None
    """

    form_dict_data = params.get('form')
    wish_type = params.get('wish')

    wish_form = var.dict_forms_status.get('form_wish')
    form_wish.update_wish_type(wish_form, wish_type)
    base_form.cambiar_pantalla('form_wish')


def iniciar_nueva_partida(form_dict_data: dict):
    """
    Reinicia el nivel actual preparando una nueva partida desde cero.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    stage = form_dict_data.get('stage')
    jugador = form_dict_data.get('jugador')
    pantalla = form_dict_data.get('screen')
    form_dict_data['stage'] = stage_juego.restart_stage(stage_data=stage, jugador=jugador, pantalla=pantalla, nro_stage=stage.get('nro_stage'))
    
    # Limpiar las etiquetas de cartas
    form_dict_data['lbl_carta_e'].update_text('', var.colores['blanco'])
    form_dict_data['lbl_carta_p'].update_text('', var.colores['blanco'])


def update_lbls_participante(form_dict_data: dict, tipo_participante: str):
    """
    Actualiza las etiquetas de estadisticas y cartas restantes de un participante.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        tipo_participante: Tipo de participante (jugador o enemigo)
        
    Returns:
        None
    """

    participante = form_dict_data.get('stage').get(tipo_participante)

    form_dict_data[f'lbl_{tipo_participante}_hp'].update_text(text=f'HP: {particip_juego.get_hp_participante(participante)}', color=var.colores['blanco'])
    form_dict_data[f'lbl_{tipo_participante}_atk'].update_text(text=f'ATK: {particip_juego.get_attack_participante(participante)}', color=var.colores['blanco'])
    form_dict_data[f'lbl_{tipo_participante}_def'].update_text(text=f'DEF: {particip_juego.get_defense_participante(participante)}', color=var.colores['blanco'])
    
    # Actualizar contador de cartas restantes
    cartas_restantes = len(particip_juego.get_cartas_restantes_participante(participante))
    form_dict_data[f'lbl_{tipo_participante}_cards'].update_text(text=f'Cards: {cartas_restantes}', color=var.colores['blanco'])
    
    # Actualizar contador de cartas restantes
    cartas_restantes = len(particip_juego.get_cartas_restantes_participante(participante))
    form_dict_data[f'lbl_{tipo_participante}_cards'].update_text(text=f'Cards: {cartas_restantes}', color=var.colores['blanco'])


def draw_bonus_widgets(form_dict_data: dict):
    """
    Dibuja los botones de bonus (heal y shield) si estan disponibles.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """

    widget_bonus = form_dict_data.get('widgets_list_bonus')
    stage = form_dict_data.get('stage')

    if stage.get('heal_available'):
        widget_bonus[0].draw()
    if stage.get('shield_available'):
        widget_bonus[1].draw()

def draw_critical_effect(form_dict_data: dict):
    """
    Dibuja el efecto visual de golpe critico en el centro de la pantalla durante un segundo.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    stage = form_dict_data.get('stage')
    if not stage:
        return
    
    tiempo_actual = pg.time.get_ticks()
    tiempo_critico = stage.get('critical_hit_time', 0)
    duracion = stage.get('critical_hit_duration', 1000)
    
    # Si paso menos de 1 segundo desde el critico, mostrar imagen
    if tiempo_actual - tiempo_critico < duracion:
        imagen = pg.image.load(var.CRITICAL_HIT).convert_alpha()
        imagen = pg.transform.scale(imagen, (var.CRITICAL_EFFECT_SIZE, var.CRITICAL_EFFECT_SIZE))
        rect = imagen.get_rect(center=(var.DIMENSION_PANTALLA[0] // 2, var.DIMENSION_PANTALLA[1] // 2 - 150))
        form_dict_data['screen'].blit(imagen, rect)

def update_bonus_widgets(form_dict_data: dict):
    """
    Actualiza el estado de los widgets de bonus segun su disponibilidad.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    widgets_bonus = form_dict_data.get('widgets_list_bonus')
    stage = form_dict_data.get('stage')
    
    if stage.get('heal_available'):
        widgets_bonus[0].update()
    if stage.get('shield_available'):
        widgets_bonus[1].update()

def draw(form_dict_data: dict):
    """
    Dibuja el formulario de stage con fondo, jugadores, widgets y efectos visuales.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    base_form.draw(form_dict_data)
    stage = form_dict_data.get('stage')
    base_form.draw_widgets(form_dict_data)
    if stage:
        stage_juego.draw_jugadores(stage)
    
    draw_bonus_widgets(form_dict_data)
    draw_critical_effect(form_dict_data)

def update_lbls_card_info(form_dict_data: dict):
    """
    Actualiza las etiquetas con la informacion de las ultimas cartas jugadas por ambos participantes.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """

    mazo_enemigo = form_dict_data.get('stage').get('enemigo').get('cartas_mazo_usadas')
    mazo_player = form_dict_data.get('stage').get('jugador').get('cartas_mazo_usadas')

    if mazo_enemigo and mazo_player:
        ultima_carta_e = particip_juego.get_carta_actual_participante(form_dict_data.get('stage').get('enemigo'))
        ultima_carta_p = particip_juego.get_carta_actual_participante(form_dict_data.get('stage').get('jugador'))
        form_dict_data['lbl_carta_e'].update_text(
            f"HP:{carta_jugador.get_hp_carta(ultima_carta_e)} ATK:{carta_jugador.get_atk_carta(ultima_carta_e)} DEF: {carta_jugador.get_def_carta(ultima_carta_e)}", pg.Color("#3597FF")
        )
        form_dict_data['lbl_carta_p'].update_text(
            f"HP:{carta_jugador.get_hp_carta(ultima_carta_p)} ATK:{carta_jugador.get_atk_carta(ultima_carta_p)} DEF: {carta_jugador.get_def_carta(ultima_carta_p)}", pg.Color("#FF8D2F")
        )

def update_score(form_dict_data: dict):
    """
    Actualiza la etiqueta del puntaje con el valor actual del jugador.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    participante = form_dict_data.get('stage').get('jugador')
    score = participante.get('score')
    form_dict_data['lbl_score'].update_text(f'Score: {score}', var.colores['blanco'])

    

def update(form_dict_data: dict, eventos: list):
    """
    Actualiza todos los elementos del formulario de stage incluyendo tiempo, cartas y verificacion de fin de juego.
    
    Args:
        form_dict_data: Diccionario con los datos del formulario
        eventos: Lista de eventos de Pygame
        
    Returns:
        None
    """
    form_dict_data['lbl_timer'].update_text(f'Time: {stage_juego.obtener_tiempo(form_dict_data.get("stage"))}', var.colores['blanco'])
    base_form.update(form_dict_data)
    stage_juego.update(form_dict_data.get("stage"))
    update_lbls_card_info(form_dict_data)
    update_lbls_participante(form_dict_data, tipo_participante='jugador')
    update_lbls_participante(form_dict_data, tipo_participante='enemigo')
    update_score(form_dict_data)

    update_bonus_widgets(form_dict_data)
    verificar_terminado(form_dict_data)
