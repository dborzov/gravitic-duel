from pygame.math import Vector2
from stupid_space_game.constants import (
    PLAYER1_UP, PLAYER1_DOWN, PLAYER1_LEFT, PLAYER1_RIGHT,PLAYER1_FIRE,
    PLAYER2_UP, PLAYER2_DOWN, PLAYER2_LEFT, PLAYER2_RIGHT,PLAYER2_FIRE,
    THRUST_ACCEL, MISSILE_GRAIN
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


def player_shoot_check(keys, world):
    if keys[PLAYER1_FIRE]:
        distance = world.rocket1.position.distance_to(world.rocket2.position)
        if MISSILE_GRAIN < distance < 10*MISSILE_GRAIN + 1:
            print(f"Not too far, not too close, ready to shoot missile")
            if abs(world.rocket1.position.x - world.rocket2.position.x) > MISSILE_GRAIN - 1:
                if abs(world.rocket1.position.y - world.rocket2.position.y) > MISSILE_GRAIN - 1:    
                    return True
        else:
            print(f"Player 1 is not ready to shoot missile: {distance}")
    return False            

