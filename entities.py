import pygame
import math
from pygame.math import Vector2
from constants import SOLAR_SYSTEM

class GameObject(pygame.sprite.Sprite):
    """Base class for all game objects."""
    
    def __init__(self, position, image=None):
        """
        Initialize a game object.
        
        Args:
            position (Vector2): The position of the object
            image (pygame.Surface, optional): The image to use for the object
        """
        super().__init__()
        self.position = position
        self.image = image
        self.rect = self.image.get_rect() if image else pygame.Rect(0, 0, 0, 0)
        self.update_rect()
    
    def update_rect(self):
        """Update the rect position based on the object's position."""
        self.rect.center = self.position

class CelestialBody(GameObject):
    """Base class for celestial bodies (star, planets, moons)."""
    
    def __init__(self, position, mass, image=None):
        """
        Initialize a celestial body.
        
        Args:
            position (Vector2): The position of the body
            mass (float): The mass value for gravity calculations
            image (pygame.Surface, optional): The image to use for the body
        """
        super().__init__(position, image)
        self.mass = mass

class Star(CelestialBody):
    """The central star in the game."""
    
    def __init__(self, position, image):
        """
        Initialize the star.
        
        Args:
            position (Vector2): The position of the star
            image (pygame.Surface): The image to use for the star
        """
        super().__init__(position, SOLAR_SYSTEM['star']['mass'], image)
    
    def update(self):
        """Update the star's state (currently nothing to update)."""
        pass

class Planet(CelestialBody):
    """A planet orbiting the star."""
    
    def __init__(self, position, mass, size, color, orbit_radius, orbit_speed, start_angle):
        """
        Initialize a planet.
        
        Args:
            position (Vector2): The initial position of the planet
            mass (float): The mass value for gravity calculations
            size (int): The diameter of the planet in pixels
            color (tuple): The RGB color of the planet
            orbit_radius (float): The radius of the planet's orbit
            orbit_speed (float): The angular speed of the planet's orbit
            start_angle (float): The initial angle of the planet in its orbit
        """
        # Create a surface for the planet
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (size//2, size//2), size//2)
        
        super().__init__(position, mass, surface)
        
        self.size = size
        self.color = color
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.angle = start_angle
        self.moons = []
    
    def update(self):
        """Update the planet's position based on its orbit."""
        # Update the angle based on orbit speed
        self.angle += self.orbit_speed
        
        # Calculate new position relative to the star
        star_pos = Vector2(
            pygame.display.get_surface().get_width() // 2 + SOLAR_SYSTEM['star']['position']['x'],
            pygame.display.get_surface().get_height() // 2 + SOLAR_SYSTEM['star']['position']['y']
        )
        self.position.x = star_pos.x + self.orbit_radius * math.cos(self.angle)
        self.position.y = star_pos.y + self.orbit_radius * math.sin(self.angle)
        
        # Update the rect
        self.update_rect()
        
        # Update all moons
        for moon in self.moons:
            moon.update(self.position)
    
    def add_moon(self, moon):
        """
        Add a moon to this planet.
        
        Args:
            moon (Moon): The moon to add
        """
        self.moons.append(moon)

class Moon(CelestialBody):
    """A moon orbiting a planet."""
    
    def __init__(self, position, planet, size, color, orbit_radius, orbit_speed, start_angle):
        """
        Initialize a moon.
        
        Args:
            position (Vector2): The initial position of the moon
            planet (Planet): The planet this moon orbits
            size (int): The diameter of the moon in pixels
            color (tuple): The RGB color of the moon
            orbit_radius (float): The radius of the moon's orbit around its planet
            orbit_speed (float): The angular speed of the moon's orbit
            start_angle (float): The initial angle of the moon in its orbit
        """
        # Create a surface for the moon
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (size//2, size//2), size//2)
        
        super().__init__(position, 0, surface)  # Moons have no gravitational effect
        
        self.planet = planet
        self.size = size
        self.color = color
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.angle = start_angle
    
    def update(self, planet_pos):
        """
        Update the moon's position based on its orbit around its planet.
        
        Args:
            planet_pos (Vector2): The current position of the planet
        """
        # Update the angle based on orbit speed
        self.angle += self.orbit_speed
        
        # Calculate new position relative to the planet
        self.position.x = planet_pos.x + self.orbit_radius * math.cos(self.angle)
        self.position.y = planet_pos.y + self.orbit_radius * math.sin(self.angle)
        
        # Update the rect
        self.update_rect() 