This document describes the final Python files and asset structure for the Gravitic Duel project repository when the game will be finished.

## Directory Layout

```
gravitic_duel/
│
├── main.py           # Main game script, entry point, game loop
├── settings.py       # General constants, configurations (screen, colors, keys, paths)
├── constants.py      # Tunable game mechanic constants (physics, entity stats, orbits)
├── entities.py       # Classes for all game objects (Rocket, Missile, Star, Planet, Moon)
├── physics.py        # Physics simulation functions (gravity, collision, movement)
├── controls.py       # Input handling logic
├── ui.py             # Functions for drawing HUD elements, messages, orbits
├── utils.py          # (Optional) Common utility functions (e.g., asset loading)
│
└── assets/
    ├── background.png
    ├── explosion.png
    ├── missile.png
    ├── rocket.png
    └── star.png
```

## File Roles

* **`main.py`**: Initializes Pygame, loads assets, sets up game objects, and manages the main game loop. Handles game state transitions (e.g., playing, round over, game over). Coordinates interactions between other modules (`controls`, `physics`, `entities`, `ui`). Processes events and manages overall game flow, including rounds and exit conditions. Can parse command-line arguments for development modes.

* **`settings.py`**: Defines non-gameplay configuration constants. Includes screen dimensions, target FPS, color definitions (RGB tuples), Pygame key mappings for controls, asset directory paths, and font settings.

* **`constants.py`**: Stores constants that directly influence gameplay mechanics and are intended for tuning. Examples include physics values (gravitational constant, elasticity for bounces), entity statistics (hit points, thrust magnitude, weapon damage, cooldown durations), game rules (maximum number of rounds), and parameters for celestial bodies (star mass, planet/moon orbital parameters, sizes, visual appearance).

* **`entities.py`**: Contains the class definitions for all dynamic game objects, such as `Rocket`, `Missile`, `Star`, `Planet`, and `Moon`. These typically inherit from a base class (e.g., `pygame.sprite.Sprite`). Each class manages its specific attributes (position, velocity, health, state) and methods (updating logic, firing mechanisms, damage handling, visual effects like explosions, orbital calculations). `Planet` and `Moon` classes might handle their own drawing (e.g., as circles).

* **`physics.py`**: Implements core physics simulation logic, detached from specific entity classes. Includes functions for calculating gravitational forces, updating entity positions and velocities based on forces and time deltas, detecting collisions between various entity types (using techniques like bounding box or circle collision), and handling collision responses (e.g., bouncing, destruction). May also handle screen boundary interactions (wrapping, despawning).

* **`controls.py`**: Provides function(s) to process player input (e.g., keyboard presses for WASD, Numpad, Fire keys, Escape). Translates raw input events into game actions or state changes (like thrust vectors, fire commands, or pause requests) to be used by `main.py` or `entities.py`.

* **`ui.py`**: Contains functions dedicated to rendering the User Interface (UI) elements onto the game screen. This includes drawing the Heads-Up Display (HUD) components (health bars, scores, timers), rendering text messages (like "Round Over", "Game Over"), and potentially visualizing game elements like orbital paths for debugging or gameplay clarity.

* **`utils.py`**: (Optional) A collection of general-purpose helper functions that could be useful across multiple modules. For instance, it might contain a robust function for loading images with error handling or color manipulation utilities.

* **`assets/images/`**: Directory storing all necessary image assets, typically in `.png` format with transparency where needed.
