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

    def draw(self, screen: pygame.Surface, position: Tuple[int, int]) -> None:
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        frame = self.frames[self.current_frame]
        screen.blit(frame, (position[0] - self.radius, position[1] - self.radius))

class RocketGraphics:
    def __init__(self) -> None:
        self.rocket_on = pygame.image.load('./assets/rocket_on.png').convert_alpha()
        self.rocket_off = pygame.image.load('./assets/rocket_off.png').convert_alpha()
        if self.rocket_on.get_size() != (50, 50):
            self.rocket_on = pygame.transform.scale(self.rocket_on, (50, 50))
        if self.rocket_off.get_size() != (50, 50):
            self.rocket_off = pygame.transform.scale(self.rocket_off, (50, 50))
        self.frames_on = []
        self.frames_off = []
        for angle in range(0, 360, 2):
            self.frames_on.append(pygame.transform.rotate(self.rocket_on, angle))
            self.frames_off.append(pygame.transform.rotate(self.rocket_off, angle))
        self.thrusters_on: bool = False
    
    def set_thrusters(self, on: bool) -> None:
        self.thrusters_on = on
    
    def draw(self, screen: pygame.Surface, position: Tuple[int, int], rotation: float = 0) -> None:
        frame_index = int(round(rotation % 360 / 2))
        sprite = self.frames_on[frame_index] if self.thrusters_on else self.frames_off[frame_index]
        sprite_rect = sprite.get_rect(center=position)
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





