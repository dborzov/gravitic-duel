import pygame
import sys
import argparse
import os
import math
from pygame.math import Vector2
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, IMG_DIR
import ui
import dev_modes
from sprites import GameSprites
from entities import Star, Planet, Moon
from constants import SOLAR_SYSTEM

# Global sprites object
sprites = None

# Sprite groups
all_sprites = None
celestial_bodies = None

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Gravitic Duel Game')
    parser.add_argument('--dev-mode', type=int, default=0,
                      help='Development mode (1-11)')
    return parser.parse_args()

def init_pygame():
    """Initialize Pygame and create the game window."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Gravitic Duel")
    clock = pygame.time.Clock()
    return screen, clock

def load_assets():
    """Load all game assets using the GameSprites class."""
    global sprites
    sprites = GameSprites()
    print("Loaded all game sprites successfully")

def setup_celestial_bodies():
    """Set up the star, planets, and moons."""
    global all_sprites, celestial_bodies
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    celestial_bodies = pygame.sprite.Group()
    
    # Create the star at the specified position
    star_pos = Vector2(
        SCREEN_WIDTH // 2 + SOLAR_SYSTEM['star']['position']['x'],
        SCREEN_HEIGHT // 2 + SOLAR_SYSTEM['star']['position']['y']
    )
    star = Star(star_pos, sprites.star)
    all_sprites.add(star)
    celestial_bodies.add(star)
    
    # Create planets and moons
    for planet_def in SOLAR_SYSTEM['planets']:
        # Calculate initial position based on orbit parameters
        initial_x = star_pos.x + planet_def['orbit_radius'] * math.cos(planet_def['start_angle'])
        initial_y = star_pos.y + planet_def['orbit_radius'] * math.sin(planet_def['start_angle'])
        initial_pos = Vector2(initial_x, initial_y)
        
        # Create the planet
        planet = Planet(
            position=initial_pos,
            mass=planet_def['mass'],
            size=planet_def['size'],
            color=planet_def['color'],
            orbit_radius=planet_def['orbit_radius'],
            orbit_speed=planet_def['orbit_speed'],
            start_angle=planet_def['start_angle']
        )
        
        all_sprites.add(planet)
        celestial_bodies.add(planet)
        
        # Create moons for this planet
        for moon_def in planet_def['moons']:
            # Calculate initial moon position
            moon_x = initial_pos.x + moon_def['orbit_radius'] * math.cos(moon_def['start_angle'])
            moon_y = initial_pos.y + moon_def['orbit_radius'] * math.sin(moon_def['start_angle'])
            moon_pos = Vector2(moon_x, moon_y)
            
            # Create the moon
            moon = Moon(
                position=moon_pos,
                planet=planet,
                size=moon_def['size'],
                color=moon_def['color'],
                orbit_radius=moon_def['orbit_radius'],
                orbit_speed=moon_def['orbit_speed'],
                start_angle=moon_def['start_angle']
            )
            
            all_sprites.add(moon)
            celestial_bodies.add(moon)
            planet.add_moon(moon)

def draw_orbit_traces(screen, center_pos):
    """Draw orbit traces for planets and moons."""
    # Draw planet orbits
    for planet_def in SOLAR_SYSTEM['planets']:
        # Create a surface for the orbit trace
        orbit_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Draw the orbit circle
        pygame.draw.circle(
            orbit_surface, 
            (*planet_def['color'], 30),  # Use planet color with low alpha
            (int(center_pos.x), int(center_pos.y)), 
            planet_def['orbit_radius'], 
            1
        )
        
        # Blit the orbit trace to the screen
        screen.blit(orbit_surface, (0, 0))
    
    # Draw moon orbits
    for planet_def in SOLAR_SYSTEM['planets']:
        if planet_def['moons']:  # If planet has moons
            # Find the planet in the celestial_bodies group
            for sprite in celestial_bodies:
                if isinstance(sprite, Planet) and sprite.orbit_radius == planet_def['orbit_radius']:
                    # Draw orbit traces for each moon
                    for moon in sprite.moons:
                        # Create a surface for the moon orbit trace
                        moon_orbit_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                        
                        # Draw the moon orbit circle
                        pygame.draw.circle(
                            moon_orbit_surface, 
                            (*moon.color, 30),  # Use moon color with low alpha
                            (int(sprite.position.x), int(sprite.position.y)), 
                            int(moon.orbit_radius), 
                            1
                        )
                        
                        # Blit the moon orbit trace to the screen
                        screen.blit(moon_orbit_surface, (0, 0))
                    break

def main():
    # Parse command line arguments
    args = parse_arguments()
    dev_mode = args.dev_mode

    # Initialize Pygame
    screen, clock = init_pygame()
    font = ui.init_font()
    
    # Load assets
    load_assets()
    
    # Set up celestial bodies if in dev mode 3
    if dev_mode == 3:
        setup_celestial_bodies()

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(BLACK)
        
        # Handle dev modes if active
        if dev_mode == 3:
            # Draw orbit traces
            center_pos = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_orbit_traces(screen, center_pos)
            
            # Update and draw celestial bodies
            for sprite in celestial_bodies:
                if isinstance(sprite, Planet):
                    sprite.update()
                elif isinstance(sprite, Star):
                    sprite.update()
            
            # Draw all sprites
            all_sprites.draw(screen)
            
            # Display dev mode text
            ui.draw_text(screen, "DEV MODE 3 ACTIVE", font)
        elif dev_mode > 0 and dev_mode != 3:
            dev_modes.handle_dev_mode(screen, dev_mode, sprites, font)

        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)

    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 