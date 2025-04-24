## Directory Layout
Here is the general layout of this game's repo.

```
stupid-space-game/
│
├── main.py           # Main game script, entry point, game loop
├── settings.py       # General configuration constants (screen resolution, colors, keys, paths)
├── constants.py      # Tunable game mechanic constants (physics, entity stats, orbits)
├── graphics.py       # Components that implement draw() with sprites and animation (stars, planets, moons, rockets) or geometric figures (orbit lines) 
├── physics.py        # Components that implement physics: orbit movement, collision, rocket movement
├── controls.py       # Components that implement input handling logic
├── entities.py       # Entities (stars, planets, moons, rockets) are defined as containers of appropriate components  
├── ui.py             # Functions for drawing HUD elements, messages, orbits
├── world.py          # Defines the world object that is a container of all the game world state and all the entities 
├── tests/            # Smaller executable scripts for manual launch that test and demonstate specific components in this repo, not for automatic testing frameworks 
│
└── assets/          # Sprites
    ├── planets/     # Sprites of celestial objects, all 100x100x pixels, 10 horizontal consequitive sprites for animation
    ├── explosion.png
    ├── missile.png
    ├── rocket.png

```
