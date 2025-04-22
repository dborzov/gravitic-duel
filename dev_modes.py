import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def handle_dev_mode(screen, dev_mode, sprites, font):
    """
    Handle different development modes.
    
    Args:
        screen: The pygame screen surface
        dev_mode (int): The current development mode
        sprites: GameSprites object containing all game sprites
        font: The pygame font object
        
    Returns:
        None
    """
    if dev_mode == 1:
        _handle_dev_mode_1(screen, font)
    elif dev_mode == 2:
        _handle_dev_mode_2(screen, sprites, font)
    elif dev_mode == 3:
        _handle_dev_mode_3(screen, sprites, font)
    # Add more dev modes here as they are implemented

def _handle_dev_mode_1(screen, font):
    """Handle dev mode 1: Display test message."""
    from ui import draw_text
    draw_text(screen, "DEV MODE 1 ACTIVE", font)

def _handle_dev_mode_2(screen, sprites, font):
    """Handle dev mode 2: Display all assets to verify transparency."""
    from ui import draw_text
    
    # Calculate center positions for assets
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    
    # Display rocket (active)
    rocket_rect = sprites.rocket.active.get_rect()
    rocket_rect.center = (center_x, center_y - 200)
    screen.blit(sprites.rocket.active, rocket_rect)
    
    # Display rocket (inactive)
    rocket_off_rect = sprites.rocket.inactive.get_rect()
    rocket_off_rect.center = (center_x, center_y - 100)
    screen.blit(sprites.rocket.inactive, rocket_off_rect)
    
    # Display missile
    missile_rect = sprites.missile.get_rect()
    missile_rect.center = (center_x, center_y)
    screen.blit(sprites.missile, missile_rect)
    
    # Display explosion
    explosion_rect = sprites.explosion.get_rect()
    explosion_rect.center = (center_x, center_y + 100)
    screen.blit(sprites.explosion, explosion_rect)
    
    # Display star
    star_rect = sprites.star.get_rect()
    star_rect.center = (center_x, center_y + 200)
    screen.blit(sprites.star, star_rect)
    
    # Display dev mode text
    draw_text(screen, "DEV MODE 2 ACTIVE", font)

def _handle_dev_mode_3(screen, sprites, font):
    """Handle dev mode 3: Display celestial bodies with orbital mechanics."""
    # This function is now handled directly in main.py
    # It's kept here for consistency with the dev mode handling structure
    pass 