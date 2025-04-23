import pygame
import math
from pygame.math import Vector2
from constants import (
    SOLAR_SYSTEM, THRUST_ACCEL, ROCKET_HP,
    FIRE_COOLDOWN_MS, MISSILE_SPEED, MISSILE_LIFETIME_S
)
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

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
        self.planets = []
        self.angle = 0  # Current rotation angle
        self.rotate_center = Vector2(
            SCREEN_WIDTH // 2 + SOLAR_SYSTEM['star']['rotate_center']['x'],
            SCREEN_HEIGHT // 2 + SOLAR_SYSTEM['star']['rotate_center']['y']
        )
        self.rotate_radius = SOLAR_SYSTEM['star']['rotate_radius']
        self.rotate_speed = SOLAR_SYSTEM['star']['rotate_speed']
    
    def update(self):
        """Update the star's state and recursively update all planets."""
        # Update the star's rotation angle
        self.angle += self.rotate_speed
        
        # Calculate new position based on rotation
        self.position.x = self.rotate_center.x + self.rotate_radius * math.cos(self.angle)
        self.position.y = self.rotate_center.y + self.rotate_radius * math.sin(self.angle)
        
        # Update the rect
        self.update_rect()
        
        # Recursively update all planets
        for planet in self.planets:
            planet.update()
    
    def add_planet(self, planet):
        """
        Add a planet to this star.
        
        Args:
            planet (Planet): The planet to add
        """
        self.planets.append(planet)

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
        self.star = None  # Reference to the star this planet orbits
    
    def update(self):
        """Update the planet's position based on its orbit."""
        # Update the angle based on orbit speed
        self.angle += self.orbit_speed
        
        # Get the star's position
        star_pos = self.star.position if self.star else Vector2(
            pygame.display.get_surface().get_width() // 2 + SOLAR_SYSTEM['star']['position']['x'],
            pygame.display.get_surface().get_height() // 2 + SOLAR_SYSTEM['star']['position']['y']
        )
        
        # Calculate new position relative to the star
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

class Rocket(GameObject):
    """A player-controlled rocket."""
    
    def __init__(self, position, player_id, image_on, image_off):
        """
        Initialize a rocket.
        
        Args:
            position (Vector2): The initial position of the rocket
            player_id (int): The ID of the player controlling this rocket (1 or 2)
            image (pygame.Surface): The image to use for the rocket
        """
        super().__init__(position, image_off)
        self.image_on = image_on
        self.image_off = image_off

        self.player_id = player_id
        self.hp = ROCKET_HP
        self.score = 0
        self.last_fire_time = 0
        self.velocity = Vector2(0, 0)
        self.rotation = 0  # Angle in degrees

    def fire(self, missile_image, explosion_image):
        """
        Fire a missile from the rocket.
        
        Args:
            missile_image (pygame.Surface): The image to use for the missile
            explosion_image (pygame.Surface): The image to use for the explosion
            
        Returns:
            Missile: The created missile object, or None if firing is on cooldown
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fire_time < FIRE_COOLDOWN_MS:
            return None
            
        # Calculate missile velocity based on rocket's velocity and direction
        direction = Vector2(math.sin(math.radians(self.rotation)), -math.cos(math.radians(self.rotation)))
        missile_velocity = self.velocity + direction * MISSILE_SPEED
        
        # Create and return the missile
        missile = Missile(self.position.copy() + 100*direction, missile_velocity, missile_image, explosion_image)
        self.last_fire_time = current_time
        return missile

    def update(self, dt, thrust_vector, gravity_vector=None):
        """
        Update the rocket's state.
        
        Args:
            dt (float): Time delta in seconds
            thrust_vector (Vector2): The thrust vector to apply
            gravity_vector (Vector2, optional): The gravitational acceleration vector to apply
        """
        # Apply thrust to velocity
        ref_image = self.image_off
        if thrust_vector.length() > 0:
            self.velocity += THRUST_ACCEL * thrust_vector * dt
            ref_image = self.image_on
            self.rotation = math.degrees(math.atan2(thrust_vector.x, -thrust_vector.y))
        elif self.velocity.length() > 0:
            self.rotation = math.degrees(math.atan2(self.velocity.x, -self.velocity.y))
            
        # Apply gravity if provided
        if gravity_vector is not None:
            self.velocity += gravity_vector * dt
        
        # Update position based on velocity
        self.position += self.velocity * dt
        
        # Screen wrapping (Atari-style)
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
            
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        
        # Update the rect
        self.update_rect()
        
        # Rotate the image
        self.image = pygame.transform.rotate(ref_image, -self.rotation)
        self.rect = self.image.get_rect(center=self.position)

class Missile(GameObject):
    """A missile fired by a rocket."""
    
    def __init__(self, position, velocity, image, explosion_image):
        """
        Initialize a missile.
        
        Args:
            position (Vector2): The initial position of the missile
            velocity (Vector2): The initial velocity of the missile
            image (pygame.Surface): The image to use for the missile
            explosion_image (pygame.Surface): The image to use for the explosion
        """
        super().__init__(position, image)
        self.velocity = velocity
        self.creation_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
        self.explosion_image = explosion_image
        self.is_exploding = False
        self.explosion_start_time = None
        self.original_image = image

    def update(self, dt, gravity_vector=None):
        """
        Update the missile's state.
        
        Args:
            dt (float): Time delta in seconds
            gravity_vector (Vector2, optional): The gravitational acceleration vector to apply
        """
        if self.is_exploding:
            # Check if explosion animation should end
            if pygame.time.get_ticks() / 1000.0 - self.explosion_start_time >= 1.0:
                self.kill()
            return

        # Check lifetime
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.creation_time >= MISSILE_LIFETIME_S:
            self.start_explosion()
            return

        # Apply gravity if provided
        if gravity_vector is not None:
            self.velocity += gravity_vector * dt
        
        self.rotation = math.degrees(math.atan2(self.velocity.x, -self.velocity.y))
        self.image = pygame.transform.rotate(self.original_image, -self.rotation)

        # Update position based on velocity
        self.position += self.velocity * dt
        
        # Update the rect
        self.update_rect()

    def start_explosion(self):
        """Start the explosion animation."""
        self.is_exploding = True
        self.explosion_start_time = pygame.time.get_ticks() / 1000.0
        self.image = self.explosion_image
        self.update_rect()