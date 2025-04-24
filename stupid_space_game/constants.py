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

COLLISION_BUFFER = 32

# --- Physics ---
ROCKET_RADIUS = 20
# General multiplier for gravitational forces. Higher values mean stronger gravity overall.
GRAVITY_FACTOR = 0.5
# Coefficient of restitution for bounces (0=inelastic, 1=perfectly elastic).
# Determines how much velocity is retained after a collision with terrain or another rocket.
BOUNCE_FACTOR = 0.6
ORBITING_SPEED_FACTOR = 0.5
# Minimum distance squared for gravity calculations to prevent extreme forces (division by zero or near-zero).
# Using distance squared avoids a square root calculation in the physics loop.
MIN_GRAVITY_DISTANCE_SQ = 25  # Avoids division by zero if distance < 5 pixels

# --- Rocket ---
# Starting health points for each player's rocket at the beginning of each round.
ROCKET_HP = 100
# The magnitude of acceleration applied per frame when a thrust key is held down.
# Higher values mean faster acceleration. This is applied along world axes (Up/Down/Left/Right).
THRUST_ACCEL = 1
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


# The solar system configuration including the central star and all celestial bodies
SOLAR_SYSTEM = {
    'star': {
        'position': {'x': 600, 'y': +600},
        'rotate_radius': 600,  
        'rotate_speed': 0.05,  # Increased by 100x
        'mass': 15000,
        'size': 500,
        'color': (255, 255, 0),  # Yellow
        'sprite_id': 'planet0-star',
    },
    'planets': [
        {
            'size': 160,
            'mass': 8000,
            'orbit_radius': 600,
            'angular_velocity': 0.05,  # Increased by 100x
            'start_angle': 47.3,
            'color': (66, 135, 245),
            'image_key': 'planet_01',
            'sprite_id': 'planet1-rock',
            'moons': []  # Blue planet with no moons
        },
        {
            'size': 100,
            'mass': 4000,
            'orbit_radius': 900,
            'angular_velocity': 0.03,  # Increased by 100x
            'start_angle': 182.7,
            'color': (245, 66, 66),
            'sprite_id': 'planet2-gas-giant',
            'moons': [
                {
                    'size': 30,
                    'mass': 500,
                    'orbit_radius': 180,  # 1.8 * planet size
                    'angular_velocity': 0.09,  # Increased by 100x
                    'start_angle': 93.2,
                    'color': (200, 200, 200),
                    'sprite_id': 'planet3-lava',
                },
                {
                    'size': 25,
                    'mass': 400,
                    'orbit_radius': 250,  # Different orbit radius
                    'angular_velocity': 0.12,  # Increased by 100x
                    'start_angle': 271.5,
                    'color': (180, 180, 180),
                    'sprite_id': 'planet4-earth',

                }
            ]
        },
        {
            'size': 130,
            'mass': 6000,
            'orbit_radius': 400,
            'angular_velocity': 0.08,  # Increased by 100x
            'start_angle': 128.4,
            'color': (66, 245, 117),
            'sprite_id': 'planet5-ice',
            'moons': [
                {
                    'size': 35,
                    'mass': 600,
                    'orbit_radius': 234,  # 1.8 * planet size
                    'angular_velocity': 0.24,  # Increased by 100x
                    'start_angle': 312.8,
                    'color': (220, 220, 220),
                    'sprite_id': 'planet6-mars',
                }
            ]
        },
        {
            'size': 90,
            'mass': 3500,
            'orbit_radius': 1200,
            'angular_velocity': 0.02,  # Increased by 100x
            'start_angle': 246.9,
            'color': (245, 188, 66),
            'sprite_id': 'planet2-gas-giant',
            'moons': [
                {
                    'size': 28,
                    'mass': 450,
                    'orbit_radius': 162,  # 1.8 * planet size
                    'angular_velocity': 0.06,  # Increased by 100x
                    'start_angle': 157.3,
                    'color': (190, 190, 190),
                    'sprite_id': 'planet7-water',
                },
                {
                    'size': 32,
                    'mass': 550,
                    'orbit_radius': 200,  # Different orbit radius
                    'angular_velocity': 0.08,  # Increased by 100x
                    'start_angle': 82.1,
                    'color': (210, 210, 210),
                    'sprite_id': 'planet6-mars',
                }
            ]
        },
        {
            'size': 110,
            'mass': 4500,
            'orbit_radius': 750,
            'angular_velocity': 0.04,  # Increased by 100x
            'start_angle': 328.4,
            'color': (188, 66, 245),
            'sprite_id': 'planet2-gas-giant',
            'moons': [
                {
                    'size': 27,
                    'mass': 420,
                    'orbit_radius': 198,  # 1.8 * planet size
                    'angular_velocity': 0.12,  # Increased by 100x
                    'start_angle': 42.7,
                    'color': (195, 195, 195),
                    'sprite_id': 'planet6-mars',
                },
                {
                    'size': 25,
                    'mass': 380,
                    'orbit_radius': 250,
                    'angular_velocity': 0.15,  # Increased by 100x
                    'start_angle': 193.6,
                    'color': (185, 185, 185),
                    'sprite_id': 'planet4-earth',
                },
                {
                    'size': 23,
                    'mass': 350,
                    'orbit_radius': 300,
                    'angular_velocity': 0.18,  # Increased by 100x
                    'start_angle': 267.9,
                    'color': (175, 175, 175),
                    'sprite_id': 'planet7-water',
                },
                {
                    'size': 21,
                    'mass': 320,
                    'orbit_radius': 350,
                    'angular_velocity': 0.21,  # Increased by 100x
                    'start_angle': 134.2,
                    'color': (165, 165, 165),
                    'sprite_id': 'planet4-earth',
                },
                {
                    'size': 19,
                    'mass': 290,
                    'orbit_radius': 400,
                    'angular_velocity': 0.24,  # Increased by 100x
                    'start_angle': 298.5,
                    'color': (155, 155, 155),
                    'sprite_id': 'planet1-rock',
                }
            ]
        },
        {
            'size': 180,  # Larger size for gas giant
            'mass': 12000,
            'orbit_radius': 2000,  # Much larger orbit
            'angular_velocity': 0.015,  # Increased by 100x
            'start_angle': 72.8,
            'color': (245, 200, 100),  # Jupiter-like color
            'sprite_id': 'planet2-gas-giant',
            'moons': [
                {
                    'size': 45,
                    'mass': 800,
                    'orbit_radius': 324,  # 1.8 * planet size
                    'angular_velocity': 0.045,  # Increased by 100x
                    'start_angle': 217.4,
                    'color': (220, 220, 220),
                    'sprite_id': 'planet1-rock',
                },
                {
                    'size': 40,
                    'mass': 700,
                    'orbit_radius': 450,
                    'angular_velocity': 0.06,  # Increased by 100x
                    'start_angle': 156.3,
                    'color': (210, 210, 210),
                    'sprite_id': 'planet1-rock',
                },
                {
                    'size': 35,
                    'mass': 600,
                    'orbit_radius': 540,
                    'angular_velocity': 0.075,  # Increased by 100x
                    'start_angle': 289.7,
                    'color': (200, 200, 200),
                    'sprite_id': 'planet4-earth',
                },
                {
                    'size': 30,
                    'mass': 500,
                    'orbit_radius': 630,
                    'angular_velocity': 0.09,  # Increased by 100x
                    'start_angle': 124.8,
                    'color': (190, 190, 190),
                    'sprite_id': 'planet7-water',
                }
            ]
        },
        {
            'size': 200,  # Even larger gas giant
            'mass': 15000,
            'orbit_radius': 3000,  # Even larger orbit
            'angular_velocity': 0.01,  # Increased by 100x
            'start_angle': 243.1,
            'color': (200, 180, 150),  # Saturn-like color
            'sprite_id': 'planet2-gas-giant',
            'moons': [
                {
                    'size': 50,
                    'mass': 900,
                    'orbit_radius': 360,
                    'angular_velocity': 0.04,  # Increased by 100x
                    'start_angle': 87.6,
                    'color': (230, 230, 230),
                    'sprite_id': 'planet1-rock',
                },
                {
                    'size': 45,
                    'mass': 800,
                    'orbit_radius': 500,
                    'angular_velocity': 0.05,  # Increased by 100x
                    'start_angle': 178.9,
                    'color': (220, 220, 220),
                    'sprite_id': 'planet3-lava',
                },
                {
                    'size': 40,
                    'mass': 700,
                    'orbit_radius': 600,
                    'angular_velocity': 0.06,  # Increased by 100x
                    'start_angle': 312.4,
                    'color': (210, 210, 210),
                    'sprite_id': 'planet4-earth',
                },
                {
                    'size': 35,
                    'mass': 600,
                    'orbit_radius': 700,
                    'angular_velocity': 0.07,  # Increased by 100x
                    'start_angle': 142.7,
                    'color': (200, 200, 200),
                    'sprite_id': 'planet7-water',
                },
                {
                    'size': 30,
                    'mass': 500,
                    'orbit_radius': 800,
                    'angular_velocity': 0.08,  # Increased by 100x
                    'start_angle': 267.3,
                    'color': (190, 190, 190),
                    'sprite_id': 'planet1-rock',
                }
            ]
        },
        {
            'size': 220,  # Largest gas giant
            'mass': 18000,
            'orbit_radius': 4000,  # Largest orbit
            'angular_velocity': 0.008,  # Increased by 100x
            'start_angle': 134.8,
            'color': (180, 160, 140),  # Uranus-like color
            'sprite_id': 'planet5-ice',
            'moons': [
                {
                    'size': 55,
                    'mass': 1000,
                    'orbit_radius': 396,
                    'angular_velocity': 0.035,  # Increased by 100x
                    'start_angle': 223.6,
                    'color': (240, 240, 240),
                    'sprite_id': 'planet3-lava',
                },
                {
                    'size': 50,
                    'mass': 900,
                    'orbit_radius': 550,
                    'angular_velocity': 0.045,  # Increased by 100x
                    'start_angle': 78.4,
                    'color': (230, 230, 230),
                    'sprite_id': 'planet1-rock',
                },
                {
                    'size': 45,
                    'mass': 800,
                    'orbit_radius': 660,
                    'angular_velocity': 0.055,  # Increased by 100x
                    'start_angle': 298.2,
                    'color': (220, 220, 220),
                    'sprite_id': 'planet1-rock',
                },
                {
                    'size': 40,
                    'mass': 700,
                    'orbit_radius': 770,
                    'angular_velocity': 0.065,  # Increased by 100x
                    'start_angle': 167.5,
                    'color': (210, 210, 210),
                    'sprite_id': 'planet4-earth',
                },
                {
                    'size': 35,
                    'mass': 600,
                    'orbit_radius': 880,
                    'angular_velocity': 0.075,  # Increased by 100x
                    'start_angle': 342.9,
                    'color': (200, 200, 200),
                    'sprite_id': 'planet7-water',
                },
                {
                    'size': 30,
                    'mass': 500,
                    'orbit_radius': 990,
                    'angular_velocity': 0.085,  # Increased by 100x
                    'start_angle': 112.3,
                    'color': (190, 190, 190),
                    'sprite_id': 'planet1-rock',
                }
            ]
        }
    ]
}
