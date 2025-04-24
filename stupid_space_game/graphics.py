from stupid_space_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
import os
from typing import List, Tuple, Optional

def init_graphics() -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
    pygame.display.set_caption("Stupid Space Game")
    return screen


class CelestialBodyGraphics:
    """
    Graphics component for celestial bodies (stars, planets, moons).
    Handles loading spritesheets and animation. Each sprite is 100x100 pixels.
    """
    def __init__(self, sprite_id: str, radius: int = 50) -> None:
        """
        Initialize the celestial body graphics component.
        
        Args:
            sprite_id (str): ID of the sprite file (without extension) in assets/planets/
            radius (int): Radius of the celestial body in pixels. If not 50, sprites will be scaled.
        """
        sprite_path = os.path.join('./assets/planets', f"{sprite_id}.png")
        self.spritesheet = pygame.image.load(sprite_path).convert_alpha()
        
        # Extract individual frames (10 frames, each 100x100)
        self.frames: List[pygame.Surface] = []
        frame_size = 2 * radius
        for i in range(10):
            frame = pygame.Surface((100, 100), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * 100, 0, 100, 100))
            if radius != 50:  # Scale if radius is not default
                frame = pygame.transform.scale(frame, (frame_size, frame_size))
            self.frames.append(frame)
        
        # Animation state
        self.current_frame: int = 0
        self.animation_speed: float = 0.1  # Frames per second
        self.animation_timer: float = 0
        self.radius = radius


    
    def draw(self, screen: pygame.Surface, position: Tuple[int, int]) -> None:
        """
        Draw the celestial body on the screen.
        
        Args:
            screen: Pygame screen to draw on
            position: (x, y) tuple for the center position
        """
        # Update animation
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        frame = self.frames[self.current_frame]
        
        
        # Draw the sprite
        screen.blit(frame, (position[0] - self.radius, position[1] - self.radius))


class RocketGraphics:
    """
    Graphics component for player rockets.
    Handles loading and displaying rocket sprites based on thruster state.
    """
    def __init__(self) -> None:
        """
        Initialize the rocket graphics component.
        Loads both thruster-on and thruster-off sprites.
        """
        # Load rocket sprites
        self.rocket_on = pygame.image.load('./assets/rocket_on.png').convert_alpha()
        self.rocket_off = pygame.image.load('./assets/rocket_off.png').convert_alpha()
        
        # Ensure sprites are 50x50
        if self.rocket_on.get_size() != (50, 50):
            self.rocket_on = pygame.transform.scale(self.rocket_on, (50, 50))
        if self.rocket_off.get_size() != (50, 50):
            self.rocket_off = pygame.transform.scale(self.rocket_off, (50, 50))
        
        # Thruster state
        self.thrusters_on: bool = False
    
    def set_thrusters(self, on: bool) -> None:
        """
        Set the thruster state.
        
        Args:
            on (bool): True if thrusters are on, False if off
        """
        self.thrusters_on = on
    
    def draw(self, screen: pygame.Surface, position: Tuple[int, int], rotation: float = 0) -> None:
        """
        Draw the rocket on the screen.
        
        Args:
            screen: Pygame screen to draw on
            position: (x, y) tuple for the center position
            rotation: Rotation angle in degrees
        """
        # Select appropriate sprite based on thruster state
        sprite = self.rocket_on if self.thrusters_on else self.rocket_off
        
        # Rotate sprite if needed
        if rotation != 0:
            sprite = pygame.transform.rotate(sprite, rotation)
        
        # Calculate position to center the sprite
        sprite_rect = sprite.get_rect(center=position)
        
        # Draw the sprite
        screen.blit(sprite, sprite_rect)

