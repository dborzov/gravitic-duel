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
    return rocket.position.distance_to(celestial.position) <= (ROCKET_RADIUS + celestial.radius)

def resolve_rocket_celestial_collision(rocket: 'Rocket', celestial: 'CelestialEntity'):
    """Resolves collision between a rocket and a celestial body by making the rocket bounce."""
    # 1. Calculate collision normal (vector from celestial center to rocket center)
    dx = rocket.position.x - celestial.position.x
    dy = rocket.position.y - celestial.position.y
    dist = math.hypot(dx, dy)
    if dist == 0: # Avoid division by zero if centers overlap perfectly
        normal_x, normal_y = 1, 0 # Default normal if overlapping
    else:
        normal_x = dx / dist
        normal_y = dy / dist

    # 2. Calculate relative velocity
    # Assuming celestial bodies are static or their velocity is negligible for bounce calculation
    relative_vx = rocket.velocity.x
    relative_vy = rocket.velocity.y

    # 3. Calculate impulse scalar (dot product of relative velocity and normal)
    impulse_scalar = relative_vx * normal_x + relative_vy * normal_y

    # 4. Calculate reflected velocity (only if moving towards each other)
    if impulse_scalar < 0:
        # Reflect velocity component along the normal
        reflect_vx = -2 * impulse_scalar * normal_x
        reflect_vy = -2 * impulse_scalar * normal_y

        # Apply bounce factor (restitution)
        rocket.velocity.x += reflect_vx * (1 + BOUNCE_FACTOR)
        rocket.velocity.y += reflect_vy * (1 + BOUNCE_FACTOR)
        

    # 5. Move rocket slightly out of collision to prevent sticking
    overlap = (ROCKET_RADIUS + celestial.radius) - dist + 1 # Small epsilon to ensure separation
    if overlap > 0:
        rocket.position.x += normal_x * overlap
        rocket.position.y += normal_y * overlap
