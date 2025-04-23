import os
import sys
from settings import IMG_DIR, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame

def _load_image(filename):
    """
    Load an image and make white pixels transparent.
    
    Args:
        filename (str): The filename of the image to load
        
    Returns:
        pygame.Surface: The loaded image with white pixels made transparent
    """
    try:
        full_path = os.path.join(IMG_DIR, filename)
        image = pygame.image.load(full_path).convert_alpha()
        
        # Create a surface with alpha channel
        surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        surface.blit(image, (0, 0))
        
        
        return surface
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image {filename}: {e}")
        sys.exit(1)  # Exit with error code 1

class RocketSprites:
    """
    Container for rocket sprites.
    
    Attributes:
        active (pygame.Surface): Rocket sprite with active thrusters
        inactive (pygame.Surface): Rocket sprite with inactive thrusters
    """
    def __init__(self, active_path, inactive_path):
        """
        Initialize rocket sprites.
        
        Args:
            active_path (str): Path to the active rocket sprite
            inactive_path (str): Path to the inactive rocket sprite
        """
        self.active = _load_image(active_path)
        self.inactive = _load_image(inactive_path)

class GameSprites:
    """
    Container for all game sprites.
    
    Attributes:
        rocket (RocketSprites): Rocket sprites (active and inactive)
        missile (pygame.Surface): Missile sprite
        explosion (pygame.Surface): Explosion sprite
        star (pygame.Surface): Star sprite
        background (pygame.Surface): Background image
    """
    def __init__(self):
        """Initialize all game sprites."""
        # Load rocket sprites
        self.rocket = RocketSprites("rocket.png", "rocket_off.png")
        
        # Load other sprites
        self.missile = _load_image("missile.png")
        self.explosion = _load_image("explosion.png")
        self.star = _load_image("star.png")
