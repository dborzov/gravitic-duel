import pygame
from pygame.math import Vector2
from settings import (
    PLAYER1_UP, PLAYER1_DOWN, PLAYER1_LEFT, PLAYER1_RIGHT,
    PLAYER2_UP, PLAYER2_DOWN, PLAYER2_LEFT, PLAYER2_RIGHT
)
from constants import THRUST_ACCEL

def process_input():
    """
    Process keyboard input and return thrust vectors for both players.
    
    Returns:
        tuple: (player1_thrust, player2_thrust) as Vector2 objects
    """
    keys = pygame.key.get_pressed()
    
    # Player 1 thrust vector
    p1_thrust = Vector2(0, 0)
    if keys[PLAYER1_UP]:
        p1_thrust.y -= THRUST_ACCEL
    if keys[PLAYER1_DOWN]:
        p1_thrust.y += THRUST_ACCEL
    if keys[PLAYER1_LEFT]:
        p1_thrust.x -= THRUST_ACCEL
    if keys[PLAYER1_RIGHT]:
        p1_thrust.x += THRUST_ACCEL
    
    # Player 2 thrust vector (not used in dev mode 4)
    p2_thrust = Vector2(0, 0)
    if keys[PLAYER2_UP]:
        p2_thrust.y -= THRUST_ACCEL
    if keys[PLAYER2_DOWN]:
        p2_thrust.y += THRUST_ACCEL
    if keys[PLAYER2_LEFT]:
        p2_thrust.x -= THRUST_ACCEL
    if keys[PLAYER2_RIGHT]:
        p2_thrust.x += THRUST_ACCEL
    
    return p1_thrust, p2_thrust 