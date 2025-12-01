"""
Modulo para control de musica y efectos de sonido del juego.
Maneja reproduccion, volumen y estado de la musica de fondo.
"""

import pygame.mixer as mixer
import pygame as pg

music_configs = {
    "actual_music_path": '',
    "current_volume": 50,
    "music_enabled": True
    
}

def set_music_path(music_path: str) -> None:
    """
    Establece la ruta de la musica actual en la configuracion.
    
    Args:
        music_path: Ruta del archivo de musica
        
    Returns:
        None
    """
    music_configs['actual_music_path'] = music_path

def play_music(loops: int = -1) -> None:
    """
    Reproduce la musica configurada si la musica esta habilitada.
    
    Args:
        loops: Numero de repeticiones 
        
    Returns:
        None
    """
    if music_configs.get('actual_music_path') and music_configs['music_enabled']:
        mixer.music.stop()  # Detener cualquier fadeout en progreso
        mixer.music.load(music_configs.get('actual_music_path'))
        mixer.music.play(loops, 0, 0)

def get_actual_volume() -> int:
    """
    Obtiene el volumen actual de la musica.
    
    Args:
        Ninguno
        
    Returns:
        int: Volumen actual en escala de 0 a 100
    """
    return music_configs["current_volume"]

def set_volume(volume: int) -> None:
    """
    Ajusta el volumen de la musica dentro del rango valido de 0 a 100.
    
    Args:
        volume: Nivel de volumen deseado
        
    Returns:
        None
    """
    actual_vol = max(0, min(100, volume))  # Asegurar que este entre 0-100
    music_configs["current_volume"] = actual_vol
    mixer.music.set_volume(actual_vol / 100)

def stop_music() -> None:
    """
    Detiene inmediatamente la reproduccion de musica.
    
    Args:
        Ninguno
        
    Returns:
        None
    """
    mixer.music.stop()  # Detener inmediatamente para poder cargar nueva musica

def set_music_enabled(enabled: bool) -> None:
    """
    Habilita o deshabilita la musica del juego con efecto de desvanecimiento al desactivar.
    
    Args:
        enabled: True para habilitar musica, False para deshabilitarla
        
    Returns:
        None
    """
    music_configs['music_enabled'] = enabled
    if not enabled:
        mixer.music.fadeout(500)  # Solo usar fadeout cuando el usuario desactiva la musica


def is_music_enabled() -> bool:
    """
    Verifica si la musica esta habilitada en la configuracion.
    
    Args:
        Ninguno
        
    Returns:
        bool: True si la musica esta habilitada, False si esta deshabilitada
    """
    return music_configs['music_enabled']