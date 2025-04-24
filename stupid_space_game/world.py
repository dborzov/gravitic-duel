from typing import Optional, Tuple, List
import pygame
import stupid_space_game.graphics as graphics
from stupid_space_game.constants import SOLAR_SYSTEM, ORBITING_SPEED_FACTOR
import math

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
        self.graphics.draw(screen, (self.position.x, self.position.y))

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


class Rocket:
    def __init__(self):
        self.position = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.rotation = 0
        self.thrusters = False
        self.graphics = graphics.RocketGraphics()

    def update(self):
        self.position += self.velocity
    
    def draw(self, screen: pygame.Surface):
        self.graphics.draw(screen, (self.position.x, self.position.y), self.rotation)

class World:
    def __init__(self):
        self._initialize_solar_system()
    
    def _initialize_solar_system(self):
        # Create the star (central body)
        star_data = SOLAR_SYSTEM['star']
        star_radius = star_data['size'] // 2  # Half of the size value
        star_graphics = graphics.CelestialBodyGraphics(star_data['sprite_id'], star_radius)
        
        # Create the star as a CelestialEntity
        self.star = CelestialEntity(
            x=star_data['position']['x'],
            y=star_data['position']['y'],
            radius=star_data['size'] // 2,
            graphics=star_graphics
        )
        
        for planet_data in SOLAR_SYSTEM['planets']:
            planet_radius = planet_data['size'] // 2
            planet_graphics = graphics.CelestialBodyGraphics(planet_data['sprite_id'], planet_radius)
            
            # Create the planet as a CelestialEntity
            planet = CelestialEntity(
                x=0,  # Initial position will be calculated based on orbit
                y=0,  # Initial position will be calculated based on orbit
                radius=planet_data['size'] // 2,
                graphics=planet_graphics,
                orbit_parent=self.star,
                orbit_radius=planet_data['orbit_radius'],
                orbit_speed=planet_data['orbit_speed'],
                orbit_angle=planet_data['start_angle']
            )
            self.star.moons.append(planet)
            
            # Create all moons for this planet
            planet_moons = []
            for moon_data in planet_data.get('moons', []):
                moon_radius = moon_data['size'] // 2
                moon_graphics = graphics.CelestialBodyGraphics(moon_data['sprite_id'], moon_radius)
                
                # Create the moon as a CelestialEntity
                moon = CelestialEntity(
                    x=0,  # Initial position will be calculated based on orbit
                    y=0,  # Initial position will be calculated based on orbit
                    radius=moon_data['size'] // 2,
                    graphics=moon_graphics,
                    orbit_parent=planet,
                    orbit_radius=moon_data['orbit_radius'],
                    orbit_speed=moon_data['orbit_speed'],
                    orbit_angle=moon_data['start_angle'],
                )
                planet_moons.append(moon)
            planet.moons = planet_moons
    
    def update(self):
        self.star.update()
    
    def draw(self, screen: pygame.Surface):
        self.star.draw(screen)





