"""
Modulo principal del juego.
Inicializa Pygame, configura la ventana del juego,
y maneja el bucle principal del juego.
"""

import sys
import pygame as pg
from modules.forms import base_form
import modules.variables as var
import modules.forms.form_controller as form_controller
import modules.particip_juego as particip_juego

def dbz_tcg():
    """
    Inicializa y ejecuta el bucle principal del juego Dragon Ball Z TCG.
    
    Args:
        Ninguno
        
    Returns:
        None
    """

    pg.init() # Inicializa todos los modulos de Pygame
    pg.display.set_caption(var.TITULO_JUEGO) # Establece el titulo de la ventana del juego
    pantalla_juego = pg.display.set_mode(var.DIMENSION_PANTALLA) # Configura el tamanio de la ventana del juego
    
    # Configurar cursor personalizado
    pg.mouse.set_visible(False)  # Ocultar cursor del sistema
    var.CURSOR_IMG = pg.image.load(var.CURSOR_PATH).convert_alpha()
    var.CURSOR_IMG = pg.transform.scale(var.CURSOR_IMG, (40, 65))

    corriendo = True # Variable para controlar el bucle principal del juego
    reloj = pg.time.Clock() # Crea un objeto Clock para controlar la velocidad de fotogramas
    datos_juegos = {
        "puntaje": 0,
        "cantidad_vidas": var.CANTIDAD_VIDAS,
        "player": particip_juego.inicializar_participante(pantalla=pantalla_juego, nombre='PLAYER'),
        "music_config": {
            "volume": var.VOLUMEN_INICIAL,
            "music_on": True
        }

    } # Diccionario para almacenar datos del juego, como puntaje y vidas.

    form_control = form_controller.create_form_controller(pantalla_juego, datos_juegos) # Crea el controlador de formularios, que maneja los diferentes formularios del juego

    while corriendo:
        eventos = pg.event.get() # Obtiene todos los eventos de Pygame (como entradas del teclado y mouse)
        reloj.tick(var.FPS) 

        for evento in eventos: 
            if evento.type == pg.QUIT:
                corriendo = False

            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    form_activo = None
                    for form in form_control['forms_list']:
                        if form['active']:
                            form_activo = form
                            break
                    if form_activo['name'] == var.FORM_NAMES['STAGE']:
                        base_form.pausar_juego()
                    elif form_activo['name'] == var.FORM_NAMES['PAUSE']:
                        base_form.despausar_juego()

        form_controller.update(form_control, eventos) # Actualiza el estado del formulario actual

        pg.display.flip() # Actualiza la pantalla completa del juego

    pg.quit()
    sys.exit()