from pygame.math import Vector2
from stupid_space_game.constants import (
    PLAYER1_UP, PLAYER1_DOWN, PLAYER1_LEFT, PLAYER1_RIGHT,
    PLAYER2_UP, PLAYER2_DOWN, PLAYER2_LEFT, PLAYER2_RIGHT,
    THRUST_ACCEL
)
from stupid_space_game.world import Rocket


def player1_input_control(keys, rocket: Rocket):
    thrust = Vector2(0, 0)
    if keys[PLAYER1_UP]:
        thrust.y -= THRUST_ACCEL
    if keys[PLAYER1_DOWN]:
        thrust.y += THRUST_ACCEL
    if keys[PLAYER1_LEFT]:
        thrust.x -= THRUST_ACCEL
    if keys[PLAYER1_RIGHT]:
        thrust.x += THRUST_ACCEL
    rocket.thrust = thrust
    

    
def player2_input_control(keys, rocket: Rocket):
    thrust = Vector2(0, 0)
    if keys[PLAYER2_UP]:
        thrust.y -= THRUST_ACCEL
    if keys[PLAYER2_DOWN]:
        thrust.y += THRUST_ACCEL
    if keys[PLAYER2_LEFT]:
        thrust.x -= THRUST_ACCEL
    if keys[PLAYER2_RIGHT]:
        thrust.x += THRUST_ACCEL
    rocket.thrust = thrust