from typing import Tuple
import pygame
import math
import stupid_space_game.graphics as graphics
from stupid_space_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLLISION_BUFFER
from stupid_space_game.constants import DEFAULT_HP

class Rocket:
    def __init__(self, x: float = 0, y: float = 0, rotation: float = 0) -> None:
        self.hp = DEFAULT_HP
        self.mana = 0.0
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.rotation = rotation
        self.thrust = pygame.math.Vector2(0, 0)
        self.thrusters = False
        self.graphics = graphics.RocketGraphics()
        self.calc_collision_rect()



    def update(self) -> None:
        if self.thrust.length() > 0:
            self.thrusters = True
            self.rotation = math.degrees(math.atan2(self.thrust.x, -self.thrust.y))
        else:
            self.thrusters = False
            self.rotation = math.degrees(math.atan2(self.velocity.x, -self.velocity.y))
            # if the rocket is too fast, slow down the rocket a bit
            if self.velocity.length() > 10:
                self.velocity *= 0.99

        self.velocity += self.thrust
        self.position += self.velocity
        # Wrap around screen edges (Atari-style)
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        self.calc_collision_rect()

    def calc_collision_rect(self):
        self.broad_borders = (
            self.position.x - COLLISION_BUFFER,
            self.position.y - COLLISION_BUFFER,
            self.position.x + COLLISION_BUFFER,
            self.position.y + COLLISION_BUFFER
        )

    def draw(self, screen: pygame.Surface) -> None:
        self.graphics.draw(screen, self.position, self.rotation, self.thrusters)


