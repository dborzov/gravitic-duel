from stupid_space_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
import os
from typing import List, Tuple, Optional
import math
def init_graphics() -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
    pygame.display.set_caption("Stupid Space Game")
    return screen

class CelestialBodyGraphics:
    def __init__(self, sprite_id: str, radius: int = 50) -> None:
        sprite_path = os.path.join('./assets/planets', f"{sprite_id}.png")
        self.spritesheet = pygame.image.load(sprite_path).convert_alpha()
        self.frames: List[pygame.Surface] = []
        frame_size = 2 * radius
        for i in range(10):
            frame = pygame.Surface((100, 100), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * 100, 0, 100, 100))
            if radius != 50:
                frame = pygame.transform.scale(frame, (frame_size, frame_size))
            self.frames.append(frame)
        self.current_frame: int = 0
        self.animation_speed: float = 0.1
        self.animation_timer: float = 0
        self.radius = radius

    def draw(self, screen: pygame.Surface, position: pygame.math.Vector2) -> None:
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        frame = self.frames[self.current_frame]
        screen.blit(frame, (position.x - self.radius, position.y - self.radius))

class RocketGraphics:
    def __init__(self) -> None:
        self.rocket_on = pygame.image.load('./assets/rocket_on.png').convert_alpha()
        self.rocket_off = pygame.image.load('./assets/rocket_off.png').convert_alpha()
        
        self.frames_on = []
        self.frames_off = []
        for angle in range(0, 360, 2):
            self.frames_on.append(pygame.transform.rotate(self.rocket_on, -angle))
            self.frames_off.append(pygame.transform.rotate(self.rocket_off, -angle))
    
    
    def draw(
        self,
        screen: pygame.Surface,
        position: pygame.math.Vector2,
        rotation: float = 0,
        thrusters_on: bool = False
    ) -> None:
        frame_index = int(round(rotation % 360 / 2))
        sprite = self.frames_on[frame_index] if thrusters_on else self.frames_off[frame_index]
        sprite_rect = sprite.get_rect(center=(position.x, position.y))
        screen.blit(sprite, sprite_rect)

class MissileGraphics:
    def __init__(self) -> None:
        self.missile = pygame.image.load('./assets/missile.png').convert_alpha()
    
    def draw(self, screen: pygame.Surface, position: Tuple[int, int], rotation: float = 0) -> None:
        sprite = self.missile
        if rotation != 0:
            sprite = pygame.transform.rotate(sprite, rotation)
        sprite_rect = sprite.get_rect(center=position)
        screen.blit(sprite, sprite_rect)



class BackgroundGraphics:
    def __init__(self) -> None:
        background = pygame.image.load('./assets/background.png').convert()
        self.oscillation_amplitude = 500
        self.background = pygame.transform.scale(background, (1000 + SCREEN_WIDTH,1000 + SCREEN_HEIGHT))
        self.oscillation_angle = 0.01

    
    def draw(self, screen: pygame.Surface) -> None:
        self.oscillation_angle += 0.003
        x = int(self.oscillation_amplitude*math.sin(self.oscillation_angle))
        y = int(self.oscillation_amplitude*math.cos(self.oscillation_angle))
        screen.blit(self.background, (-500 + x, -500 + y))


