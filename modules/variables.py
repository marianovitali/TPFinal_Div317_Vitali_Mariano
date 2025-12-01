"""
Modulo de constantes y configuraciones globales del juego.
Define dimensiones, rutas de recursos, colores y parametros de juego.
"""

import pygame as pg

########## Dimensiones y Configuraciones Generales ##########
DIMENSION_PANTALLA = (1600, 900)
TITULO_JUEGO = 'Dragon Ball Z TCG'
FPS = 30
dict_forms_status = {}
STAGE_TIMER = 60
JSON_CONFIGS = 'configs.json'
JSON_INFO_CARDS = 'info_cartas.json'
VOLUMEN_INICIAL = 50
CANTIDAD_VIDAS = 3

########## Configuracion de Cartas ##########
CARTA_SIZE_NORMAL = 50
CARTA_SIZE_HOVER = 70

########## Sistema de Combate ##########
CRITICAL_HIT_CHANCE = 0.25  # 25% de probabilidad
CRITICAL_DAMAGE_MULTIPLIER = 5
CRITICAL_HIT_DURATION = 1000  # milisegundos
CRITICAL_EFFECT_SIZE = 400

########## Interfaz ##########
MAX_NAME_LENGTH = 6
PAUSE_VOLUME = 0.1

########## Fuentes ##########
FONT_AKSARAKOMIK = 'assets/fonts/AksaraKomik-Regular.ttf'

########## FORMS ##########
FORM_NAMES = {
    'MENU': 'form_menu',
    'RANKING': 'form_ranking', 
    'OPTIONS': 'form_options',
    'BATTLE': 'form_battle',
    'CHARACTER_SELECT': 'form_character',
    'PAUSE': 'form_pause',
    'STAGE': 'form_stage',
    'NAME': 'form_name',
    'WISH': 'form_wish'
}

########## Fondos de formularios ##########
FONDO_MENU = 'assets/img/background/mainmenu.png'
FONDO_RANKING = 'assets/img/background/ranking.png'
FONDO_OPTIONS = 'assets/img/background/configuracion.png'
FONDO_PAUSE = 'assets/img/background/pause.png'
FONDO_STAGE = 'assets/img/background/stage.png'
FONDO_NAME = 'assets/img/background/victory.png'
FONDO_WISH = 'assets/img/background/wish.png'
FONDO_VICTORY = 'assets/img/background/victory.png'
FONDO_DEFEAT = 'assets/img/background/defeat.png'
CRITICAL_HIT = 'assets/img/fx/critico.png'

########## Imagenes Botones ##########
IMG_EXIT = 'assets/img/buttons/boton-salir.png'
IMG_MENU = 'assets/img/buttons/menu-principal.png'
IMG_CONFIG = 'assets/img/buttons/boton-config.png'
CURSOR_PATH = 'assets/img/cursor/dbz_cursor.png'
CURSOR_IMG = None  
IMG_RADAR_AZUL = 'assets/img/background/radar-azul.png'
IMG_RADAR_NARANJA = 'assets/img/background/radar-naranja.png'
IMG_BTN_PLAY = 'assets/img/buttons/boton-jugar.png'
IMG_BTN_HEAL = 'assets/img/buttons/boton-heal.png'
IMG_BTN_SHIELD = 'assets/img/buttons/boton-shield.png'

########## Archivos ##########
RANKING_CSV = 'puntajes.csv'


########## Colores ##########
colores = {
    "amarillo": pg.Color('yellow'),
    "azul": pg.Color('blue'),
    "blanco": pg.Color('white'),
    "cian": pg.Color('cyan'),
    "naranja": pg.Color('orange'),
    "negro": pg.Color('black'),
    "rojo": pg.Color('red'),
    "rosa": pg.Color('pink'),
    "verde": pg.Color('green')
}

# Fondo y musica para el formulario de opciones
MUSICA_RANKING = 'assets/sound/ranking.mp3'
MUSICA_MENU = 'assets/sound/mainmenu.mp3'
MUSICA_OPTIONS = 'assets/sound/mainmenu.mp3'
MUSICA_PAUSE = 'assets/sound/battle.mp3'
MUSICA_STAGE = 'assets/sound/battle.mp3'
MUSICA_VICTORY = 'assets/sound/victory.mp3'
MUSICA_DEFEAT = 'assets/sound/defeat.mp3'
SOUND_CRITICAL_HIT = 'assets/sound/critical.wav'