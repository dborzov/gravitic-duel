from typing import Optional, List
import pygame
import math
import stupid_space_game.graphics as graphics
from stupid_space_game.constants import ORBITING_SPEED_FACTOR, SCREEN_WIDTH, SCREEN_HEIGHT

BROAD_CHECK_COOLOFF = 100
class CelestialEntity:
    def __init__(
        self,
        x: float,
        y: float,
        radius: int,
        graphics: graphics.CelestialBodyGraphics,
        orbit_parent: Optional['CelestialEntity'] = None,
        orbit_radius: float = 0.0,
        angular_velocity: float = 0.0,
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
        self.angular_velocity = angular_velocity
        self.orbit_angle = orbit_angle
        self.moons = []
        self.broad_check_cooldown = 0
        self.calc_broad_borders()

    def update(self) -> None:
        if self.orbit_parent is not None:
            # Update the orbit angle based on orbit speed
            self.orbit_angle += ORBITING_SPEED_FACTOR*self.angular_velocity
            
            # Calculate the new position based on circular orbit
            # Using parametric equations for a circle: x = center_x + radius * cos(angle), y = center_y + radius * sin(angle)
            self.position = pygame.math.Vector2(
                self.orbit_parent.position.x + self.orbit_radius * math.cos(self.orbit_angle),
                self.orbit_parent.position.y + self.orbit_radius * math.sin(self.orbit_angle)
            )
        self.calc_broad_borders()
        for moon in self.moons:
            moon.update()

    def orbit_speed(self) -> float:
        return self.angular_velocity * ORBITING_SPEED_FACTOR * self.orbit_radius

    def orbit_velocity(self) -> pygame.math.Vector2:
        return pygame.math.Vector2(
            self.orbit_speed() * math.cos(self.orbit_angle),
            self.orbit_speed() * math.sin(self.orbit_angle)
        )

    def draw(self, screen: pygame.Surface) -> None:
        if self.broad_check_cooldown > 0:
            self.broad_check_cooldown -= 1
            return
        else:
            if not is_on_screen_broad_check(self, self.orbit_speed()* BROAD_CHECK_COOLOFF):
                self.broad_check_cooldown = BROAD_CHECK_COOLOFF
                return

        if self.orbit_parent is not None:
            # Draw orbit trace as a semi-transparent circle
            orbit_surface = pygame.Surface((self.orbit_radius * 2, self.orbit_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                orbit_surface,
                (255, 255, 255, 34),
                (self.orbit_radius, self.orbit_radius),
                self.orbit_radius,
                3 # Line width
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

    def calc_broad_borders(self):
        self.broad_borders = (
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.position.x + self.radius,
            self.position.y + self.radius
        )




def is_on_screen_broad_check(celestial: CelestialEntity, buffer_size: int) -> bool:
    # Calculate the boundaries of the expanded screen area
    extended_min_x = 0 - buffer_size
    extended_max_x = SCREEN_WIDTH + buffer_size
    extended_min_y = 0 - buffer_size
    extended_max_y = SCREEN_HEIGHT + buffer_size    

    # Calculate the planet's bounding box edges
    planet_min_x = celestial.position.x - celestial.radius
    planet_max_x = celestial.position.x + celestial.radius
    planet_min_y = celestial.position.y - celestial.radius
    planet_max_y = celestial.position.y + celestial.radius

    # Check for non-overlap. The planet is *definitely* off-screen if:
    # Its right edge is left of the extended screen's left edge OR
    if planet_max_x < extended_min_x: return False
    # Its left edge is right of the extended screen's right edge OR
    if planet_min_x > extended_max_x: return False
    # Its bottom edge is above the extended screen's top edge OR
    if planet_max_y < extended_min_y: return False
    # Its top edge is below the extended screen's bottom edge
    if planet_min_y > extended_max_y: return False

    # If none of the non-overlap conditions were met, there is potential overlap.
    return True    