import pygame
import math
from typing import TYPE_CHECKING
from stupid_space_game.constants import ROCKET_RADIUS
# Avoid circular imports for type hinting
if TYPE_CHECKING:
    from stupid_space_game.rockets import Rocket
    from stupid_space_game.celestials import CelestialEntity

BOUNCE_FACTOR = 0.7 # Restitution factor (0=no bounce, 1=perfect bounce)

def check_rocket_celestial_collision(rocket: 'Rocket', celestial: 'CelestialEntity') -> bool:
    if celestial.broad_check_cooldown > 0:
        return False
    if not is_probably_colliding_broad_check(rocket, celestial):
        return False
    return rocket.position.distance_to(celestial.position) <= (ROCKET_RADIUS + celestial.radius)
    

def is_probably_colliding_broad_check(rocket: 'Rocket', celestial: 'CelestialEntity') -> bool:
    if rocket.broad_borders[2] < celestial.broad_borders[0]:
        return False
    if rocket.broad_borders[0] > celestial.broad_borders[2]:
        return False
    if rocket.broad_borders[3] < celestial.broad_borders[1]:
        return False
    if rocket.broad_borders[1] > celestial.broad_borders[3]:
        return False
    return True


def resolve_rocket_celestial_collision(rocket: 'Rocket', celestial: 'CelestialEntity'):
    """Resolves collision between a rocket and a celestial body by making the rocket bounce."""
    # 1. Calculate collision normal (vector from celestial center to rocket center)
    if rocket.position == celestial.position:
        return None
    normal = rocket.position - celestial.position
    if normal.length() < ROCKET_RADIUS + celestial.radius:
        rocket.position = celestial.position + normal.normalize() * (ROCKET_RADIUS + celestial.radius)

    normal = normal.normalize()
    
    
    # 2. Calculate relative velocity
    # Assuming celestial bodies are static or their velocity is negligible for bounce calculation
    relative_v = rocket.velocity + celestial.orbit_velocity()
    
    # 3. Calculate impulse scalar (dot product of relative velocity and normal)
    impulse_scalar = relative_v.dot(normal)
    
    # charges manna proprotional to the impulse
    rocket.mana += abs(impulse_scalar* 0.3) 
    if rocket.mana > 100.0:
        rocket.mana = 100.0

    # 4. Calculate reflected velocity (only if moving towards each other)
    if impulse_scalar < 0:
        # Reflect velocity component along the normal
        reflect_v = normal * (-2 * impulse_scalar)
        rocket.velocity += reflect_v

