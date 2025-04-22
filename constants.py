# Description: Centralized game mechanic constants for the game.
# These values are intended to be tweaked for gameplay balancing and tuning.

import math

# --- Physics ---
# General multiplier for gravitational forces. Higher values mean stronger gravity overall.
GRAVITY_FACTOR = 0.05
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
THRUST_ACCEL = 0.8
# The minimum time in milliseconds that must pass between firing missiles.
FIRE_COOLDOWN_MS = 2500

# --- Missile ---
# The constant speed at which missiles travel. Missiles are not affected by thrust.
MISSILE_SPEED = 12.0
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
STAR_MASS_PROXY = 15000

# List defining the properties of each planet. Each element is a dictionary:
#   'size': Diameter in pixels (used for visual representation and potentially gravity scaling).
#   'mass_proxy': Value representing 'mass' for gravity calculations.
#   'moons': Number of moons orbiting this planet.
#   'orbit_radius': Distance from the central star (or screen center) in pixels.
#   'orbit_speed': Angular speed in radians per frame (determines how fast it orbits).
#   'start_angle': Initial angle in radians (0 is typically to the right).
#   'color': RGB tuple for the planet's visual color.
#   'image_key': String key to look up the specific planet image file (e.g., 'planet_01').
PLANET_DEFINITIONS = [
    {'size': 160, 'mass_proxy': 8000, 'moons': 0, 'orbit_radius': 600, 'orbit_speed': 0.0005, 'start_angle': math.pi / 2, 'color': (66, 135, 245), 'image_key': 'planet_01'}, # Blue, Medium Orbit
    {'size': 100, 'mass_proxy': 4000, 'moons': 2, 'orbit_radius': 900, 'orbit_speed': 0.0003, 'start_angle': 0, 'color': (245, 66, 66), 'image_key': 'planet_02'}, # Red, Wider Orbit
    {'size': 130, 'mass_proxy': 6000, 'moons': 1, 'orbit_radius': 400, 'orbit_speed': 0.0008, 'start_angle': math.pi, 'color': (66, 245, 117), 'image_key': 'planet_03'}, # Green, Closer Orbit
    {'size': 90, 'mass_proxy': 3500, 'moons': 2, 'orbit_radius': 1200, 'orbit_speed': 0.0002, 'start_angle': 3 * math.pi / 2, 'color': (245, 188, 66), 'image_key': 'planet_04'}, # Orange, Widest Orbit
    {'size': 110, 'mass_proxy': 4500, 'moons': 5, 'orbit_radius': 750, 'orbit_speed': 0.0004, 'start_angle': math.pi / 4, 'color': (188, 66, 245), 'image_key': 'planet_05'}, # Purple, Mid-Wide Orbit
]

# Visual diameter of moons in pixels.
MOON_SIZE = 30
# 'Mass' proxy for moons (set to 0 to have no gravitational effect).
MOON_MASS_PROXY = 0
# Factor determining moon orbit radius relative to planet size (e.g., 1.5 * planet radius).
MOON_ORBIT_RADIUS_FACTOR = 1.8
# Factor determining moon orbit speed relative to planet orbit speed (e.g., 2.0 * planet speed).
MOON_ORBIT_SPEED_FACTOR = 3.0
