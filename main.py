import pygame
import sys
import argparse
import os
import math
from pygame.math import Vector2
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, IMG_DIR
import ui
import dev_modes
import controls
import physics
from sprites import GameSprites
from entities import Star, Planet, Moon, Rocket
from constants import SOLAR_SYSTEM, ROCKET_HP

# Global sprites object
sprites = None

# Sprite groups
all_entities = None
star = None
rocket1, rocket2 = None, None
missiles = None

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
    global all_entities, star
    # Create sprite groups
    all_entities = pygame.sprite.Group()
    
    # Calculate the star's initial position based on rotation parameters
    star_pos = Vector2(
        SCREEN_WIDTH // 2 + SOLAR_SYSTEM['star']['rotate_center']['x'] + SOLAR_SYSTEM['star']['rotate_radius'],
        SCREEN_HEIGHT // 2 + SOLAR_SYSTEM['star']['rotate_center']['y']
    )
    star = Star(star_pos, sprites.star)
    all_entities.add(star)
    
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
        
        # Link planet to star
        planet.star = star
        star.add_planet(planet)
        
        all_entities.add(planet)
        
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
            
            all_entities.add(moon)
            planet.add_moon(moon)


def setup_players():
    """Set up the player rockets."""
    global all_entities, rocket1, rocket2, missiles
    
    # Create sprite groups
    missiles = pygame.sprite.Group()
    
    # Create Player 1's rocket
    p1_pos = Vector2(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    rocket1 = Rocket(p1_pos, 1, sprites.rocket.active, sprites.rocket.inactive)
    rocket1.original_image = sprites.rocket.active
    rocket1.hp = ROCKET_HP
    all_entities.add(rocket1)
    
    # Create Player 2's rocket (not used in dev mode 4)
    p2_pos = Vector2(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    rocket2 = Rocket(p2_pos, 2, sprites.rocket.active, sprites.rocket.inactive)
    rocket2.original_image = sprites.rocket.active
    rocket2.hp = ROCKET_HP
    all_entities.add(rocket2)


def draw_orbit_traces(star):
    """Draw orbit traces for planets and moons."""
    # Create a surface for drawing orbits with alpha transparency
    orbit_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    # Draw orbits for each planet
    for planet in star.planets:
        # Draw planet orbit around the star
        pygame.draw.circle(
            orbit_surface,
            (*planet.color, 30),  # Use planet color with low alpha
            (int(star.position.x), int(star.position.y)),
            planet.orbit_radius,
            1
        )
        
        # Draw orbits for each moon around its planet
        for moon in planet.moons:
            # Draw moon orbit around its planet
            pygame.draw.circle(
                orbit_surface,
                (*moon.color, 30),  # Use moon color with low alpha
                (int(planet.position.x), int(planet.position.y)),
                moon.orbit_radius,
                1
            )
    return orbit_surface
    

def get_gravity_bodies():
    """Get a list of celestial bodies that exert gravity (star and planets)."""
    bodies = [star]  # Star always exerts gravity
    bodies.extend(star.planets)  # Add all planets
    return bodies

def main():
    global all_entities, star, rocket1, rocket2, missiles
    # Parse command line arguments
    args = parse_arguments()
    dev_mode = args.dev_mode

    # Initialize Pygame
    screen, clock = init_pygame()
    font = ui.init_font()
    
    # Load assets
    load_assets()
    print("Step 1: Assets were loaded")
    # Set up celestial bodies if in dev mode 3 or 4
    if dev_mode in [3, 4]:
        setup_celestial_bodies()
    print("Step 2: Celestial bodies were setup")
    # Set up players if in dev mode 4
    if dev_mode == 4:
        print("Step 3: Players were setup")
        setup_players()
    # Main game loop
    print("Step 4: Main game loop started")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Handle firing
                elif event.key == pygame.K_q:  # Player 1 fire
                    missile = rocket1.fire(sprites.missile, sprites.explosion)
                    if missile:
                        missiles.add(missile)
                        all_entities.add(missile)
                elif event.key == pygame.K_KP7:  # Player 2 fire
                    missile = rocket2.fire(sprites.missile, sprites.explosion)
                    if missile:
                        missiles.add(missile)
                        all_entities.add(missile)

        screen.fill(BLACK)

        # Update celestial bodies
        star.update()
        
        # Get input and time delta
        p1_thrust, p2_thrust = controls.process_input()
        dt = clock.get_time() / 1000.0  # Convert to seconds
        
        # Get gravity-exerting bodies
        gravity_bodies = get_gravity_bodies()
        
        # Calculate and apply gravity to rockets
        p1_gravity = physics.calculate_gravity_acceleration(rocket1.position, gravity_bodies)
        p2_gravity = physics.calculate_gravity_acceleration(rocket2.position, gravity_bodies)
        
        # Update rockets with gravity
        rocket1.update(dt, p1_thrust, p1_gravity)
        rocket2.update(dt, p2_thrust, p2_gravity)
        
        # Check screen wrapping
        physics.check_screen_wrap(rocket1, SCREEN_WIDTH, SCREEN_HEIGHT)
        physics.check_screen_wrap(rocket2, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Update missiles
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        for missile in list(missiles):  # Create a copy of the list to safely modify during iteration
            missile_gravity = physics.calculate_gravity_acceleration(missile.position, gravity_bodies)
            missile.update(dt, missile_gravity)
            if physics.check_missile_despawn(missile, screen_rect):
                missile.kill()  # This removes it from all sprite groups it belongs to

        # Draw all entities
        all_entities.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 