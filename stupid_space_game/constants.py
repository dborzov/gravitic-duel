# Description: Centralized game mechanic constants for the game.
# These values are intended to be tweaked for gameplay balancing and tuning.

import math
import pygame


# Screen settings
SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1440
FPS = 60



# Key mappings
PLAYER1_UP = pygame.K_w
PLAYER1_DOWN = pygame.K_s
PLAYER1_LEFT = pygame.K_a
PLAYER1_RIGHT = pygame.K_d
PLAYER1_FIRE = pygame.K_q

PLAYER2_UP = pygame.K_KP8
PLAYER2_DOWN = pygame.K_KP2
PLAYER2_LEFT = pygame.K_KP4
PLAYER2_RIGHT = pygame.K_KP6
PLAYER2_FIRE = pygame.K_KP7


# --- Physics ---
# General multiplier for gravitational forces. Higher values mean stronger gravity overall.
GRAVITY_FACTOR = 0.5
# Coefficient of restitution for bounces (0=inelastic, 1=perfectly elastic).
# Determines how much velocity is retained after a collision with terrain or another rocket.
BOUNCE_FACTOR = 0.6
# Minimum distance squared for gravity calculations to prevent extreme forces (division by zero or near-zero).
# Using distance squared avoids a square root calculation in the physics loop.
MIN_GRAVITY_DISTANCE_SQ = 25  # Avoids division by zero if distance < 5 pixels

# --- Rocket ---
# Starting health points for each player's rocket at the beginning of each round.
ROCKET_HP = 100
# The magnitude of acceleration applied per frame when a thrust key is held down.
# Higher values mean faster acceleration. This is applied along world axes (Up/Down/Left/Right).
THRUST_ACCEL = 10
# The minimum time in milliseconds that must pass between firing missiles.
FIRE_COOLDOWN_MS = 2500

# --- Missile ---
# The constant speed at which missiles travel. Missiles are not affected by thrust.
MISSILE_SPEED = 42.0

# Maximum duration in seconds a missile can exist before self-destructing.
MISSILE_LIFETIME_S = 30.0
# The amount of HP damage inflicted when a missile hits an opponent's rocket.
MISSILE_DAMAGE = 25

# --- Collisions ---
# Scaling factor to determine HP damage from collisions (Rocket-Terrain, Rocket-Rocket).
# Damage = magnitude of relative velocity * COLLISION_DAMAGE_SCALE
COLLISION_DAMAGE_SCALE = 0.2

# --- Game Rules ---
# The total number of rounds played in a single game.
MAX_ROUNDS = 5

# --- Celestial Bodies ---
# Represents the 'mass' of the central star for gravity calculations. Larger value = stronger pull.
STAR_MASS = 15000

# The solar system configuration including the central star and all celestial bodies
SOLAR_SYSTEM = {
    'star': {
        'rotate_center': {'x': -600, 'y': +600},  # Center of the screen
        'rotate_radius': 600,  
        'rotate_speed': 0.0005,  
        'mass': STAR_MASS,
        'size': 200,
        'color': (255, 255, 0)  # Yellow
    },
    'planets': [
        {
            'size': 160,
            'mass': 8000,
            'orbit_radius': 600,
            'orbit_speed': 0.0005,
            'start_angle': math.pi / 2,
            'color': (66, 135, 245),
            'image_key': 'planet_01',
            'moons': []  # Blue planet with no moons
        },
        {
            'size': 100,
            'mass': 4000,
            'orbit_radius': 900,
            'orbit_speed': 0.0003,
            'start_angle': 0,
            'color': (245, 66, 66),
            'image_key': 'planet_02',
            'moons': [
                {
                    'size': 30,
                    'mass': 500,
                    'orbit_radius': 180,  # 1.8 * planet size
                    'orbit_speed': 0.0009,  # 3.0 * planet speed
                    'start_angle': 0,
                    'color': (200, 200, 200)
                },
                {
                    'size': 25,
                    'mass': 400,
                    'orbit_radius': 250,  # Different orbit radius
                    'orbit_speed': 0.0012,  # Different orbit speed
                    'start_angle': math.pi / 3,
                    'color': (180, 180, 180)
                }
            ]
        },
        {
            'size': 130,
            'mass': 6000,
            'orbit_radius': 400,
            'orbit_speed': 0.0008,
            'start_angle': math.pi,
            'color': (66, 245, 117),
            'image_key': 'planet_03',
            'moons': [
                {
                    'size': 35,
                    'mass': 600,
                    'orbit_radius': 234,  # 1.8 * planet size
                    'orbit_speed': 0.0024,  # 3.0 * planet speed
                    'start_angle': math.pi / 4,
                    'color': (220, 220, 220)
                }
            ]
        },
        {
            'size': 90,
            'mass': 3500,
            'orbit_radius': 1200,
            'orbit_speed': 0.0002,
            'start_angle': 3 * math.pi / 2,
            'color': (245, 188, 66),
            'image_key': 'planet_04',
            'moons': [
                {
                    'size': 28,
                    'mass': 450,
                    'orbit_radius': 162,  # 1.8 * planet size
                    'orbit_speed': 0.0006,  # 3.0 * planet speed
                    'start_angle': 0,
                    'color': (190, 190, 190)
                },
                {
                    'size': 32,
                    'mass': 550,
                    'orbit_radius': 200,  # Different orbit radius
                    'orbit_speed': 0.0008,  # Different orbit speed
                    'start_angle': math.pi / 2,
                    'color': (210, 210, 210)
                }
            ]
        },
        {
            'size': 110,
            'mass': 4500,
            'orbit_radius': 750,
            'orbit_speed': 0.0004,
            'start_angle': math.pi / 8,
            'color': (188, 66, 245),
            'image_key': 'planet_05',
            'moons': [
                {
                    'size': 27,
                    'mass': 420,
                    'orbit_radius': 198,  # 1.8 * planet size
                    'orbit_speed': 0.0012,  # 3.0 * planet speed
                    'start_angle': 0,
                    'color': (195, 195, 195)
                },
                {
                    'size': 25,
                    'mass': 380,
                    'orbit_radius': 250,
                    'orbit_speed': 0.0015,
                    'start_angle': math.pi / 3,
                    'color': (185, 185, 185)
                },
                {
                    'size': 23,
                    'mass': 350,
                    'orbit_radius': 300,
                    'orbit_speed': 0.0018,
                    'start_angle': 2 * math.pi / 3,
                    'color': (175, 175, 175)
                },
                {
                    'size': 21,
                    'mass': 320,
                    'orbit_radius': 350,
                    'orbit_speed': 0.0021,
                    'start_angle': math.pi,
                    'color': (165, 165, 165)
                },
                {
                    'size': 19,
                    'mass': 290,
                    'orbit_radius': 400,
                    'orbit_speed': 0.0024,
                    'start_angle': 4 * math.pi / 3,
                    'color': (155, 155, 155)
                }
            ]
        },
        {
            'size': 180,  # Larger size for gas giant
            'mass': 12000,
            'orbit_radius': 2000,  # Much larger orbit
            'orbit_speed': 0.00015,
            'start_angle': math.pi / 6,
            'color': (245, 200, 100),  # Jupiter-like color
            'image_key': 'planet_06',
            'moons': [
                {
                    'size': 45,
                    'mass': 800,
                    'orbit_radius': 324,  # 1.8 * planet size
                    'orbit_speed': 0.00045,
                    'start_angle': 0,
                    'color': (220, 220, 220)
                },
                {
                    'size': 40,
                    'mass': 700,
                    'orbit_radius': 450,
                    'orbit_speed': 0.0006,
                    'start_angle': math.pi / 4,
                    'color': (210, 210, 210)
                },
                {
                    'size': 35,
                    'mass': 600,
                    'orbit_radius': 540,
                    'orbit_speed': 0.00075,
                    'start_angle': math.pi / 2,
                    'color': (200, 200, 200)
                },
                {
                    'size': 30,
                    'mass': 500,
                    'orbit_radius': 630,
                    'orbit_speed': 0.0009,
                    'start_angle': 3 * math.pi / 4,
                    'color': (190, 190, 190)
                }
            ]
        },
        {
            'size': 200,  # Even larger gas giant
            'mass': 15000,
            'orbit_radius': 3000,  # Even larger orbit
            'orbit_speed': 0.0001,
            'start_angle': 2 * math.pi / 3,
            'color': (200, 180, 150),  # Saturn-like color
            'image_key': 'planet_07',
            'moons': [
                {
                    'size': 50,
                    'mass': 900,
                    'orbit_radius': 360,
                    'orbit_speed': 0.0004,
                    'start_angle': 0,
                    'color': (230, 230, 230)
                },
                {
                    'size': 45,
                    'mass': 800,
                    'orbit_radius': 500,
                    'orbit_speed': 0.0005,
                    'start_angle': math.pi / 3,
                    'color': (220, 220, 220)
                },
                {
                    'size': 40,
                    'mass': 700,
                    'orbit_radius': 600,
                    'orbit_speed': 0.0006,
                    'start_angle': 2 * math.pi / 3,
                    'color': (210, 210, 210)
                },
                {
                    'size': 35,
                    'mass': 600,
                    'orbit_radius': 700,
                    'orbit_speed': 0.0007,
                    'start_angle': math.pi,
                    'color': (200, 200, 200)
                },
                {
                    'size': 30,
                    'mass': 500,
                    'orbit_radius': 800,
                    'orbit_speed': 0.0008,
                    'start_angle': 4 * math.pi / 3,
                    'color': (190, 190, 190)
                }
            ]
        },
        {
            'size': 220,  # Largest gas giant
            'mass': 18000,
            'orbit_radius': 4000,  # Largest orbit
            'orbit_speed': 0.00008,
            'start_angle': 5 * math.pi / 6,
            'color': (180, 160, 140),  # Uranus-like color
            'image_key': 'planet_08',
            'moons': [
                {
                    'size': 55,
                    'mass': 1000,
                    'orbit_radius': 396,
                    'orbit_speed': 0.00035,
                    'start_angle': 0,
                    'color': (240, 240, 240)
                },
                {
                    'size': 50,
                    'mass': 900,
                    'orbit_radius': 550,
                    'orbit_speed': 0.00045,
                    'start_angle': math.pi / 4,
                    'color': (230, 230, 230)
                },
                {
                    'size': 45,
                    'mass': 800,
                    'orbit_radius': 660,
                    'orbit_speed': 0.00055,
                    'start_angle': math.pi / 2,
                    'color': (220, 220, 220)
                },
                {
                    'size': 40,
                    'mass': 700,
                    'orbit_radius': 770,
                    'orbit_speed': 0.00065,
                    'start_angle': 3 * math.pi / 4,
                    'color': (210, 210, 210)
                },
                {
                    'size': 35,
                    'mass': 600,
                    'orbit_radius': 880,
                    'orbit_speed': 0.00075,
                    'start_angle': math.pi,
                    'color': (200, 200, 200)
                },
                {
                    'size': 30,
                    'mass': 500,
                    'orbit_radius': 990,
                    'orbit_speed': 0.00085,
                    'start_angle': 5 * math.pi / 4,
                    'color': (190, 190, 190)
                }
            ]
        }
    ]
}
