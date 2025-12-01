"""
Modulo principal para gestion de niveles del juego.
Controla la logica de combate, temporizador, condiciones de victoria y reparticion de cartas.
"""

import pygame as pg
import modules.variables as var
import modules.auxiliar as aux
import random as rd
import modules.carta as carta
import modules.particip_juego as particip_juego

def inicializar_stage(jugador: dict, pantalla: pg.Surface, nro_stage: int):
    """
    Crea e inicializa un nuevo nivel del juego con todos sus parametros y participantes.
    
    Args:
        jugador: Diccionario con los datos del jugador
        pantalla: Superficie de Pygame donde se dibujara el nivel
        nro_stage: Numero del nivel a inicializar
        
    Returns:
        dict: Diccionario con todos los datos del nivel inicializado
    """
    stage_data = {}
    stage_data['nro_stage'] = nro_stage
    stage_data['configs'] = {}
    stage_data['data_cargada'] = False
    
    stage_data['mazo_completo'] = []

    stage_data['ruta_mazo'] = ''
    stage_data['screen'] = pantalla
    
    stage_data['jugador'] = jugador


    stage_data['coords_inicial_mazo_enemigo'] = (450, 100)
    stage_data['coords_final_mazo_enemigo'] = (950, 100)

    stage_data['coords_inicial_mazo_player'] = (450, 500)
    stage_data['coords_final_mazo_player'] = (950, 500)

    stage_data['enemigo'] = particip_juego.inicializar_participante(stage_data.get('screen'), nombre='Enemigo')
    particip_juego.setear_stat_participante(stage_data.get('enemigo'), 'pos_deck_inicial', stage_data.get('coords_inicial_mazo_enemigo'))
    particip_juego.setear_stat_participante(stage_data.get('enemigo'), 'pos_deck_jugados', stage_data.get('coords_final_mazo_enemigo'))

    particip_juego.setear_stat_participante(stage_data.get('jugador'), 'pos_deck_inicial', stage_data.get('coords_inicial_mazo_player'))
    particip_juego.setear_stat_participante(stage_data.get('jugador'), 'pos_deck_jugados', stage_data.get('coords_final_mazo_player'))

    stage_data['heal_available'] = True
    stage_data['shield_available'] = True
    stage_data['shield_activo'] = False
    stage_data["cantidad_cartas_jugadores"] = 0
    

    stage_data['juego_finalizado'] = False
    stage_data['stage_timer'] = var.STAGE_TIMER
    stage_data['last_timer'] = pg.time.get_ticks()
    stage_data['ganador'] = None
    stage_data['critical_hit_time'] = 0
    stage_data['critical_hit_duration'] = var.CRITICAL_HIT_DURATION

    return stage_data


def modificar_estado_bonus(stage_data: dict, bonus: str):
    """
    Marca un bonus como no disponible despues de ser usado.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        bonus: Nombre del bonus a desactivar (heal o shield)
        
    Returns:
        None: Modifica la disponibilidad del bonus directamente
    """
    stage_data[f'{bonus}_available'] = False

def timer_update(stage_data: dict):
    """
    Actualiza el temporizador del nivel decrementandolo cada segundo.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        None: Modifica el temporizador directamente
    """
    if stage_data['stage_timer'] > 0:
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - stage_data.get('last_timer', 0) > 1000:
            stage_data['stage_timer'] -= 1
            stage_data['last_timer'] = tiempo_actual

def obtener_tiempo(stage_data: dict):
    """
    Obtiene el tiempo restante del temporizador del nivel.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        int: Segundos restantes en el temporizador
    """
    return stage_data.get('stage_timer')

def barajar_y_repartir_cartas(stage_data: dict):
    """
    Mezcla el mazo completo y reparte cartas aleatorias a ambos jugadores.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        None: Modifica stage_data asignando cartas a jugador y enemigo
    """
    if not stage_data.get('juego_finalizado'):
        print('Barajando y repartiendo cartas...')
        
        # Mezclar todo el mazo
        rd.shuffle(stage_data.get('mazo_completo'))
        cant_cartas = stage_data.get("cantidad_cartas_jugadores")
        
        # Repartir al jugador
        cartas_jugador = rd.sample(stage_data.get('mazo_completo'), cant_cartas)
        particip_juego.set_cartas_participante(stage_data.get('jugador'), cartas_jugador)
        
        # Remover cartas ya asignadas y repartir al enemigo
        mazo_restante = [c for c in stage_data.get('mazo_completo') if c not in cartas_jugador]
        cartas_enemigo = rd.sample(mazo_restante, cant_cartas)
        particip_juego.set_cartas_participante(stage_data.get('enemigo'), cartas_enemigo)

        # Asignar stats iniciales
        particip_juego.asignar_stats_iniciales_participante(stage_data.get('jugador'))
        particip_juego.asignar_stats_iniciales_participante(stage_data.get('enemigo'))

        stage_data['data_cargada'] = True

def inicializar_data_stage(stage_data: dict):
    """
    Carga las configuraciones y mazos del nivel y prepara el juego para comenzar.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        None: Modifica stage_data cargando todas las configuraciones necesarias
    """
    print('Inicializando data del stage...')

    aux.cargar_configs_stage(stage_data) # Leer la config del juego desde un archivo
    aux.cargar_y_preparar_mazos(stage_data)  # Cargar mazos directamente en mazo_completo
    barajar_y_repartir_cartas(stage_data)  # Barajar y repartir a ambos jugadores


def hay_jugadores_con_cartas(stage_data: dict) -> bool:
    """
    Verifica si al menos un jugador tiene cartas disponibles para jugar.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        bool: True si hay jugadores con cartas, False si ambos se quedaron sin cartas
    """
    jugador_con_cartas = particip_juego.get_cartas_restantes_participante(stage_data.get('jugador'))
    enemigo_con_cartas = particip_juego.get_cartas_restantes_participante(stage_data.get('enemigo'))
    return jugador_con_cartas or enemigo_con_cartas

def restart_stage(stage_data: dict, jugador: dict, pantalla: pg.Surface, nro_stage: int):
    """
    Reinicia el nivel actual restaurando todos los valores a su estado inicial.
    
    Args:
        stage_data: Diccionario con los datos del nivel actual
        jugador: Diccionario con los datos del jugador
        pantalla: Superficie de Pygame donde se dibujara el nivel
        nro_stage: Numero del nivel a reiniciar
        
    Returns:
        dict: Nuevo diccionario con el nivel reinicializado
    """
    print('Reiniciando stage...')
    stage_data = inicializar_stage(jugador, pantalla, nro_stage)
    particip_juego.reiniciar_datos_participante(jugador)
    inicializar_data_stage(stage_data)

    return stage_data

def jugar_mano(stage_data: dict):
    """
    Ejecuta una ronda de juego donde ambos participantes juegan una carta y se compara el danio.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        tuple: Tupla con dos valores (critical, ganador_mano) o None si el juego finalizo
    """
    if not stage_data.get('juego_finalizado'):
        jugar_mano_stage(stage_data)

        critical, ganador_mano = comparar_damage(stage_data)

        chequear_ganador(stage_data)

        return critical, ganador_mano
    return None

def jugar_mano_stage(stage_data: dict):
    """
    Hace que ambos participantes jueguen su siguiente carta.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        None: Modifica los mazos de ambos participantes
    """
    particip_juego.jugar_carta(stage_data.get('jugador'))
    particip_juego.jugar_carta(stage_data.get('enemigo'))


def es_golpe_gritico() -> bool:
    """
    Determina aleatoriamente si un golpe es critico.
    
    Args:
        Ninguno
        
    Returns:
        bool: True si el golpe es critico, False en caso contrario
    """
    critical = rd.choice([False, False, False, True])
    return critical


def comparar_damage(stage_data: dict):
    """
    Compara el ataque de las cartas jugadas y aplica el danio al perdedor de la ronda.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        tuple: Tupla con (critical, ganador_mano) indicando si hubo critico y quien gano
    """
    ganador_mano = None
    
    jugador = stage_data.get('jugador')
    enemigo = stage_data.get('enemigo')
    critical = False
    carta_jugador = particip_juego.get_carta_actual_participante(jugador)
    carta_enemigo = particip_juego.get_carta_actual_participante(enemigo)

    if carta_enemigo and carta_jugador:
        critical = es_golpe_gritico()
        
        # Obtener ATK base y aplicar bonus de estrellas
        atk_jugador_base = carta.get_atk_carta(carta_jugador)
        atk_enemigo_base = carta.get_atk_carta(carta_enemigo)
        
        atk_jugador = carta.calcular_bonus_estrellas(carta_jugador, atk_jugador_base)
        atk_enemigo = carta.calcular_bonus_estrellas(carta_enemigo, atk_enemigo_base)
        
        estrellas_j = carta.get_estrellas_carta(carta_jugador)
        estrellas_e = carta.get_estrellas_carta(carta_enemigo)
        
        print(f'[JUGADOR] ATK base: {atk_jugador_base} | Estrellas: {estrellas_j} | ATK con bonus: {atk_jugador} (+{atk_jugador - atk_jugador_base})')
        print(f'[ENEMIGO] ATK base: {atk_enemigo_base} | Estrellas: {estrellas_e} | ATK con bonus: {atk_enemigo} (+{atk_enemigo - atk_enemigo_base})')

        if atk_enemigo > atk_jugador:
            ganador_mano = 'PC'
            
            # SHIELD: si esta activo, refleja el danio al enemigo
            if stage_data.get('shield_activo'):
                print('SHIELD ACTIVADO! El danio se refleja al enemigo')
                particip_juego.restar_stats_participante(enemigo, carta_enemigo, critical)
                stage_data['shield_activo'] = False
            else:
                particip_juego.restar_stats_participante(jugador, carta_enemigo, critical)
            
            if critical:
                print('GOLPE CRITICO! El enemigo hizo danio x4')
        else:
            score = atk_jugador - carta.get_def_carta(carta_enemigo)
            ganador_mano = 'PLAYER'
            particip_juego.restar_stats_participante(enemigo, carta_jugador, critical)
            particip_juego.add_score_participante(jugador, score)
            if critical:
                print('GOLPE CRITICO! El jugador hizo danio x4')


    return critical, ganador_mano

def setear_ganador(stage_data: dict, participante: dict):
    """
    Establece al ganador del nivel y suma puntos extra por tiempo restante.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        participante: Participante que gano el nivel
        
    Returns:
        None: Modifica stage_data estableciendo al ganador y finalizando el juego
    """
    puntaje_extra = stage_data['stage_timer']
    puntaje_actual = particip_juego.get_score_participante(participante)
    particip_juego.add_score_participante(participante, puntaje_extra)
    puntaje_actual_nuevo = particip_juego.get_score_participante(participante)
    print(f'Puntaje extra por tiempo restante: {puntaje_extra}. Puntaje total: {puntaje_actual_nuevo}')
    stage_data['ganador'] = participante
    stage_data['juego_finalizado'] = True

def chequear_ganador(stage_data: dict):
    """
    Verifica las condiciones de victoria y determina si hay un ganador.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        None: Modifica stage_data si se cumplen condiciones de victoria
    """
    jugador = stage_data.get('jugador')
    enemigo = stage_data.get('enemigo')
    
    hp_j = particip_juego.get_hp_participante(jugador)
    hp_e = particip_juego.get_hp_participante(enemigo)
    cartas_j = len(particip_juego.get_cartas_restantes_participante(jugador))
    cartas_e = len(particip_juego.get_cartas_restantes_participante(enemigo))
    timer = stage_data['stage_timer']
    
    # REGLA 2: HP = 0 (maxima prioridad)
    if hp_j <= 0:
        setear_ganador(stage_data, enemigo)
        return
    if hp_e <= 0:
        setear_ganador(stage_data, jugador)
        return
    
    # REGLA 3: Timer = 0 - mayor HP gana
    if timer <= 0:
        if hp_j > hp_e:
            setear_ganador(stage_data, jugador)
        elif hp_e > hp_j:
            setear_ganador(stage_data, enemigo)
        return
    
    # REGLA 1: Sin cartas + HP inferior
    if cartas_j == 0 and hp_j < hp_e:
        setear_ganador(stage_data, enemigo)
        return
    if cartas_e == 0 and hp_e < hp_j:
        setear_ganador(stage_data, jugador)
        return

def esta_finalizado(stage_data: dict) -> bool:
    """
    Verifica si el juego ha finalizado.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        bool: True si el juego finalizo, False si aun continua
    """
    return stage_data.get('juego_finalizado')

def obtener_ganador(stage_data: dict) -> bool:
    """
    Obtiene el participante que gano el nivel.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        dict: Diccionario del participante ganador
    """
    return stage_data.get('ganador')


def draw_jugadores(stage_data: dict):
    """
    Dibuja las cartas de ambos participantes en pantalla.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        None: Dibuja los participantes en la pantalla
    """
    mouse_pos = pg.mouse.get_pos()
    particip_juego.draw_participante(stage_data.get('jugador'), stage_data.get('screen'), mouse_pos)
    particip_juego.draw_participante(stage_data.get('enemigo'), stage_data.get('screen'), mouse_pos)


def update(stage_data: dict):
    """
    Actualiza el estado del nivel verificando el temporizador y condiciones de victoria.
    
    Args:
        stage_data: Diccionario con los datos del nivel
        
    Returns:
        None: Modifica el estado del nivel
    """
    timer_update(stage_data)
    chequear_ganador(stage_data)