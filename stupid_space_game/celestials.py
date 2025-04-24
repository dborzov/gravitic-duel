from typing import Optional, List
import pygame
import math
import stupid_space_game.graphics as graphics
from stupid_space_game.constants import ORBITING_SPEED_FACTOR

class CelestialEntity:
    def __init__(
        self,
        x: float,
        y: float,
        radius: int,
        graphics: graphics.CelestialBodyGraphics,
        orbit_parent: Optional['CelestialEntity'] = None,
        orbit_radius: float = 0.0,
        orbit_speed: float = 0.0,
        orbit_angle: float = 0.0,
    ):
        self.radius = radius
        self.graphics = graphics
        if orbit_parent is not None:
            self.position = pygame.math.Vector2(
                orbit_parent.position.x + orbit_radius * math.cos(orbit_angle),
                orbit_parent.position.y + orbit_radius * math.sin(orbit_angle)
            )
        else:
            self.position = pygame.math.Vector2(x, y)
        self.orbit_parent = orbit_parent
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.orbit_angle = orbit_angle
        self.moons = []

    def draw(self, screen: pygame.Surface) -> None:
        if self.orbit_parent is not None:
            # Draw orbit trace as a semi-transparent circle
            orbit_surface = pygame.Surface((self.orbit_radius * 2, self.orbit_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                orbit_surface,
                (255, 255, 255, 34),  # White with 25% opacity
                (self.orbit_radius, self.orbit_radius),
                self.orbit_radius,
                3  # Line width of 1 pixel
            )
            screen.blit(
                orbit_surface,
                (
                    self.orbit_parent.position.x - self.orbit_radius,
                    self.orbit_parent.position.y - self.orbit_radius
                )
            )
        self.graphics.draw(screen, self.position)

        for moon in self.moons:
            moon.draw(screen)

    def update(self) -> None:
        if self.orbit_parent is not None:
            # Update the orbit angle based on orbit speed
            self.orbit_angle += ORBITING_SPEED_FACTOR*self.orbit_speed
            
            # Calculate the new position based on circular orbit
            # Using parametric equations for a circle: x = center_x + radius * cos(angle), y = center_y + radius * sin(angle)
            self.position = pygame.math.Vector2(
                self.orbit_parent.position.x + self.orbit_radius * math.cos(self.orbit_angle),
                self.orbit_parent.position.y + self.orbit_radius * math.sin(self.orbit_angle)
            )
        for moon in self.moons:
            moon.update()
