"""
Modulo base para todos los formularios del juego.
Provee funciones comunes para crear, actualizar, dibujar y gestionar transiciones entre formularios.
"""

import pygame as pg
import modules.variables as var
import modules.sonido as sonido

def create_base_form(dict_form_data: dict) -> dict:
    """
    Crea un formulario base con sus propiedades fundamentales de pantalla y musica.
    
    Args:
        dict_form_data: Diccionario con los datos de configuracion del formulario
        
    Returns:
        dict: Formulario inicializado con todas sus propiedades base
    """
    
    form = {}

    form['name'] = dict_form_data['name']
    form['screen'] = dict_form_data.get('screen')
    form['active'] = dict_form_data.get('active')
    form['music_path'] = dict_form_data.get('music_path')
    form['surface'] = pg.image.load(dict_form_data.get('background')).convert_alpha()
    form['surface'] = pg.transform.scale(form.get('surface'), dict_form_data.get('screen_dimensions'))

    form['rect'] = form.get('surface').get_rect()
    form['rect'].x = dict_form_data.get('coord')[0]
    form['rect'].y = dict_form_data.get('coord')[1]
    form['music_config'] = dict_form_data.get('music_config')
    
    return form

def draw_widgets(form_data: dict):
    """
    Dibuja todos los widgets contenidos en la lista de widgets del formulario.
    
    Args:
        form_data: Diccionario con los datos del formulario
        
    Returns:
        None: Dibuja los widgets en pantalla
    """
    for widget in form_data.get('widgets_list'):
        widget.draw()

def update_widgets(form_data: dict):
    """
    Actualiza el estado de todos los widgets del formulario.
    
    Args:
        form_data: Diccionario con los datos del formulario
        
    Returns:
        None: Actualiza cada widget
    """

    for widget in form_data.get('widgets_list'):
        try:
            widget.update([])
        except TypeError:
            widget.update()

def set_active(form_name: str):
    """
    Activa un formulario especifico y desactiva todos los demas.
    
    Args:
        form_name: Nombre del formulario a activar
        
    Returns:
        None: Modifica el estado de los formularios
    """
    for form in var.dict_forms_status.values():
        form['active'] = False
    var.dict_forms_status[form_name]['active'] = True



def cambiar_pantalla(form_name: str):
    """
    Cambia al formulario especificado limpiando eventos y reproduciendo su musica.
    
    Args:
        form_name: Nombre del formulario al que se desea cambiar
        
    Returns:
        None: Activa el nuevo formulario y reproduce su musica
    """
    # Limpiar eventos de mouse
    pg.event.clear(pg.MOUSEBUTTONDOWN)
    pg.event.clear(pg.MOUSEBUTTONUP)
    
    set_active(form_name)

    # Reproducir musica del nuevo formulario activo
    form_activo = var.dict_forms_status.get(form_name)
    if form_activo:
        music_on(form_activo)

        
def pausar_juego():
    """
    Pausa el juego reduciendo el volumen de la musica y cambiando a la pantalla de pausa.
    
    Args:
        Ninguno
        
    Returns:
        None
    """
    form_pause = var.dict_forms_status.get(var.FORM_NAMES['PAUSE'])
    form_pause['previous_volume'] = pg.mixer.music.get_volume()
    pg.mixer.music.set_volume(var.PAUSE_VOLUME)
    cambiar_pantalla(var.FORM_NAMES['PAUSE'])

def despausar_juego(param=None):
    """
    Reanuda el juego restaurando el volumen de la musica y volviendo al nivel.
    
    Args:
        param: Parametro opcional no utilizado
        
    Returns:
        None
    """
    form_pause = var.dict_forms_status.get(var.FORM_NAMES['PAUSE'])
    if form_pause.get('previous_volume') is not None:
        pg.mixer.music.set_volume(form_pause['previous_volume'])
    cambiar_pantalla(var.FORM_NAMES['STAGE'])

def salir_de_pause(destino: str):
    """
    Sale del menu de pausa restaurando el volumen y cambiando a la pantalla destino.
    
    Args:
        destino: Nombre del formulario destino
        
    Returns:
        None
    """
    form_pause = var.dict_forms_status.get(var.FORM_NAMES['PAUSE'])
    if form_pause.get('previous_volume') is not None:
        pg.mixer.music.set_volume(form_pause['previous_volume'])
    cambiar_pantalla(destino)

def music_on(form_data: dict):
    """
    Reproduce la musica del formulario si esta habilitada y es diferente a la actual.
    
    Args:
        form_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    music_path = form_data.get('music_path')
    music_cfg = form_data.get('music_config', {})
    
    if not music_path or not sonido.is_music_enabled():
        return  # No reproducir si musica esta desactivada globalmente   
    
    # Solo cambiar si es una musica diferente
    if sonido.music_configs.get('actual_music_path') != music_path:
        sonido.set_music_path(music_path)
        loops = music_cfg.get('loops', -1)  # Por defecto infinito
        sonido.play_music(loops)
    # Si es la misma musica, no hacer nada (se mantiene sonando)

def draw_cursor(screen: pg.Surface):
    """
    Dibuja el cursor personalizado en la posicion actual del mouse.
    
    Args:
        screen: Superficie de Pygame donde se dibujara el cursor
        
    Returns:
        None
    """
    mouse_pos = pg.mouse.get_pos()
    screen.blit(var.CURSOR_IMG, mouse_pos)

def update(form_data: dict):
    """
    Actualiza todos los widgets del formulario.
    
    Args:
        form_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    update_widgets(form_data)

def draw(form_data: dict):
    """
    Dibuja el fondo del formulario en la pantalla.
    
    Args:
        form_data: Diccionario con los datos del formulario
        
    Returns:
        None
    """
    form_data['screen'].blit(form_data.get('surface'), form_data.get('rect'))