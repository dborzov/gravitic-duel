import pygame
import math
from constants import GRAVITY_FACTOR, MIN_GRAVITY_DISTANCE_SQ

def calculate_gravity_acceleration(entity_pos, celestial_bodies):
    """
    Calculate gravitational acceleration vector for an entity based on nearby celestial bodies.
    Uses inverse square law: F = G * (m1 * m2) / r^2
    
    Args:
        entity_pos: pygame.Vector2 position of the entity
        celestial_bodies: List of celestial bodies (star and planets) with position and mass
        
    Returns:
        pygame.Vector2 acceleration vector
    """
    total_accel = pygame.Vector2(0, 0)
    
    for body in celestial_bodies:
        # Calculate direction vector from entity to celestial body
        direction = body.position - entity_pos
        distance_sq = direction.length_squared()
        
        # Skip if too close to avoid division by zero
        if distance_sq < MIN_GRAVITY_DISTANCE_SQ:
            continue
            
        # Normalize direction and scale by inverse square law
        # F = G * m / r^2 where G is GRAVITY_FACTOR
        force_magnitude = GRAVITY_FACTOR * body.mass / distance_sq
        total_accel += direction.normalize() * force_magnitude
        
    return total_accel

def check_screen_wrap(entity, screen_width, screen_height):
    """
    Check if entity has gone off screen and wrap it to the other side if needed.
    
    Args:
        entity: Entity with position attribute (pygame.Vector2)
        screen_width: Width of the game screen
        screen_height: Height of the game screen
    """
    if entity.position.x < 0:
        entity.position.x = screen_width
    elif entity.position.x > screen_width:
        entity.position.x = 0
        
    if entity.position.y < 0:
        entity.position.y = screen_height
    elif entity.position.y > screen_height:
        entity.position.y = 0 

def check_missile_despawn(missile, screen_rect):
    """
    Check if a missile should be despawned due to being off-screen.
    
    Args:
        missile (Missile): The missile to check
        screen_rect (pygame.Rect): The screen boundaries
        
    Returns:
        bool: True if the missile should be despawned, False otherwise
    """
    return not screen_rect.colliderect(missile.rect) 