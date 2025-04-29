from typing import Optional, Tuple, List
import pygame
import stupid_space_game.graphics as graphics
from stupid_space_game.constants import SOLAR_SYSTEM, ORBITING_SPEED_FACTOR, SCREEN_WIDTH, SCREEN_HEIGHT
import math
from stupid_space_game.celestials import CelestialEntity
from stupid_space_game.rockets import Rocket
import stupid_space_game.physics as physics
from stupid_space_game.constants import DEFAULT_HP
from stupid_space_game.ui import draw_fighter_health_bars

class World:
    def __init__(self):
        self._celestials: List[CelestialEntity] = []
        self._initialize_solar_system()
        self.rocket1 = Rocket(
            x=SCREEN_WIDTH // 4,
            y=2 * SCREEN_HEIGHT // 3,
            rotation=270,
        )
        self.rocket2 = Rocket(
            x=3 * SCREEN_WIDTH // 4, 
            y=1 * SCREEN_HEIGHT // 3,
            rotation=90,
        )
    
    def _initialize_solar_system(self):
        star_data = SOLAR_SYSTEM['star']
        star_radius = star_data['size'] // 2
        star_graphics = graphics.CelestialBodyGraphics(
            star_data['sprite_id'], 
            2*star_radius # the specific sprite of the star is 2x the others 
        )
        
        self.star = CelestialEntity(
            x=star_data['position']['x'],
            y=star_data['position']['y'],
            radius=star_data['size'] // 2,
            graphics=star_graphics
        )
        self._celestials.append(self.star)
        
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
                angular_velocity=planet_data['angular_velocity'],
                orbit_angle=planet_data['start_angle']
            )
            self.star.moons.append(planet)
            self._celestials.append(planet)
            
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
                    angular_velocity=moon_data['angular_velocity'],
                    orbit_angle=moon_data['start_angle'],
                )
                planet_moons.append(moon)
                self._celestials.append(moon)
            planet.moons = planet_moons
    
    def update(self):
        self.star.update()
        self.rocket1.update()
        self.rocket2.update()
        
        for celestial in self._celestials:
            if physics.check_rocket_celestial_collision(self.rocket1, celestial):
                physics.resolve_rocket_celestial_collision(self.rocket1, celestial)
                break
        for celestial in self._celestials:
            if physics.check_rocket_celestial_collision(self.rocket2, celestial):
                physics.resolve_rocket_celestial_collision(self.rocket2, celestial)
                break
    
    def draw(self, screen: pygame.Surface):
        self.star.draw(screen)
        self.rocket1.draw(screen)
        self.rocket2.draw(screen)
        draw_fighter_health_bars(screen, self.rocket1.hp, DEFAULT_HP, self.rocket2.hp, DEFAULT_HP)






