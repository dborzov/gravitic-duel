# Gravitic Duel - Development Plan (PLAN.md)

This document outlines the step-by-step process for building the Gravitic Duel Pygame project. Each step provides instructions suitable for a coding LLM, resulting in a testable state via `--dev-mode` arguments. Assume the LLM has access to `SPEC.md` and `FILES.md`.

## Running the Game

1.  **Setup:** Navigate to the project's parent directory.
2.  **Environment:** `python3 -m venv venv && source venv/bin/activate`
3.  **Dependencies:** `pip install pygame`
4.  **Run:** `python3 gravitic_duel/main.py [--dev-mode=N]`

---

## Development Steps

### Step 0: Project Setup

* **Instruction:** Create the project directory structure as defined in `FILES.md`. Create empty Python files. Place the specified image assets (`background.png`, `explosion.png`, `missile.png`, `rocket.png`, `star.png`) in `assets/images/`. Populate `settings.py` and `constants.py` with their initial content (as provided separately or in previous context). Set up and activate a Python virtual environment and install Pygame.

<br><br>

### Step 1: Basic Window & UI Text (`--dev-mode=1`)

* **Instruction:** Let's implement dev-mode=1. In `main.py`, initialize Pygame, create a fullscreen window (2560x1440) and clock as per `settings.py`. Add basic argument parsing for `--dev-mode`. Implement the main loop with event handling for quitting (`ESC` key and window close). In `ui.py`, implement `init_font()` and `draw_text()` for rendering centered text. In `main.py`, if `dev_mode == 1`, fill the screen black and use `ui.draw_text` to display a static test message (e.g., "DEV MODE 1 ACTIVE") centered. Ensure `pygame.display.flip()` and `clock.tick()` are called. Add cleanup (`pygame.quit()`).

<br><br>

### Step 2: Asset Loading & Background (`--dev-mode=2`)

* **Instruction:** Implement dev-mode=2 by implementing the loading of image assets. Create an asset loading mechanism. Use `utils.py` for a `load_image` function handling path joining (`settings.IMG_DIR`) and loading (`pygame.image.load`, `convert_alpha()`). In `main.py`, create a global `assets` dictionary. Implement `load_assets()` to load all images specified in `SPEC.md`/`FILES.md` into the `assets` dict using their base filenames as keys (e.g., `assets['background']`). Call `load_assets()` once after `pygame.init()`. Modify the main loop: always blit `assets['background']` first. If `dev_mode == 2`, show all the assets in the background so that it can be verified that the transparent parts are indeed rendered transparently.

<br><br>

### Step 3: Celestial Bodies (`--dev-mode=3`)


Implement everyting needed for dev-mode=3 where entities and physics of all the entities that do not depend on the players are defined.


Specifically, implement everything needed for planets, moons and the star inside `entities.py` and in the main loop.

Define `GameObject(pygame.sprite.Sprite)` base class storing `position` (Vector2), `image`, `rect`. 

Define `CelestialBody(GameObject)` storing `mass_proxy`. Define `Star(CelestialBody)`. Define `Planet(CelestialBody)` storing orbit parameters (`orbit_radius`, `orbit_speed`, `start_angle` from `constants.py`), color, and size. Define `Moon(CelestialBody)` similarly, storing reference to its parent planet. In `main.py`, create sprite groups (`all_sprites`, `celestial_bodies`). Implement `setup_celestial_bodies(assets)`: Create the `Star` instance at screen center. Iterate through `constants.PLANET_DEFINITIONS`: Calculate initial static position, create `Planet` instance (pass color, size, position; *do not* load image), add to groups. For each planet's moons, calculate static position relative to planet, create `Moon` instance (pass color, size, position), add to groups. Call this setup function. In the main loop, draw `all_sprites`. 

Make updates to the positions of planets and moons in the main game loop.

Make everything so that when launching the game the following is shown:
**Expected View:** Planets orbit the star, and moons orbit the planets. The planets and moons are drawn as differently colored circles. There are subtle semi-transparent orbit traces as cirlces giving the player a hint of where the orbit is. Each game loop tick the positions of all these entities are updated.
 **Interaction:** Pressing `ESC` or closing the window quits. No other interaction.

<br><br>

### Step 4: Orbiting Celestial Bodies (`--dev-mode=4`)

* **Instruction:** Implement Step 4. In `entities.py`, add `update(dt)` methods to `Planet` and `Moon`. Implement circular orbit logic: update internal angle based on `orbit_speed`, recalculate `position` vector based on angle, radius, and center of orbit (star's position for planets, parent planet's current position for moons). Update `self.rect.center` from `self.position`. In `main.py`, calculate `dt` (time delta) each frame. Call `all_sprites.update(dt)` in the main loop before drawing. Ensure planets update before moons if needed. For dev mode 4, show background and orbiting bodies.

<br><br>

### Step 5: Static Rockets (`--dev-mode=5`)

* **Instruction:** Implement Step 5. In `entities.py`, define `Rocket(GameObject)` storing `player_id`, `hp`, `score`, `last_fire_time`, `velocity` (Vector2). In `main.py`, create `rockets` group. In `load_assets`, ensure `assets['rocket']` is loaded. Implement `setup_players(assets)`: Create two `Rocket` instances at specified start positions using `assets['rocket']`, add them to `all_sprites` and `rockets`. Call this setup function. For dev mode 5, show background, orbiting bodies, and static rockets.

<br><br>

### Step 6: Rocket Control & Basic Movement (`--dev-mode=6`)

* **Instruction:** Implement Step 6. In `controls.py`, implement `process_input()` checking pressed keys (`settings` for key maps) and returning thrust vectors (Vector2) for each player based on `constants.THRUST_ACCEL`. In `entities.py`, modify `Rocket.update(dt, thrust_vector)`: Apply thrust to velocity (`velocity += thrust_vector * dt`), update position (`position += velocity * dt`), update rect center. In `main.py`, get thrust vectors from `controls.process_input()`. Update rockets individually by calling their `update` method, passing the respective thrust vector and `dt`. For dev mode 6, enable rocket movement via WASD/Numpad.

<br><br>

### Step 7: Gravity & Screen Wrap (`--dev-mode=7`)

* **Instruction:** Implement Step 7. In `physics.py`, implement `calculate_gravity_acceleration(entity_pos, celestial_bodies)` using inverse square law based on `mass_proxy` and distance, scaled by `GRAVITY_FACTOR`, avoiding division by zero (`MIN_GRAVITY_DISTANCE_SQ`), summing vectors from star and on-screen planets. Implement `check_screen_wrap(entity)` for rockets, modifying `entity.position`. In `entities.py`, modify `Rocket.update` to accept and apply `gravity_vector` to velocity (`velocity += gravity_vector * dt`). In `main.py`, for each rocket, calculate its gravity using `physics.calculate_gravity_acceleration`, pass it to the rocket's `update` method, and then call `physics.check_screen_wrap`. For dev mode 7, rockets should be affected by gravity and wrap screen edges.

<br><br>

### Step 8: Missile System (`--dev-mode=8`)

* **Instruction:** Implement Step 8. In `entities.py`, define `Missile(GameObject)` storing `owner_id`, `creation_time`, `velocity`. Implement `Missile.update(dt, gravity_vector)`: apply gravity, update position, check lifetime (`constants.MISSILE_LIFETIME_S`) and `self.kill()` if expired. In `controls.py`, modify `process_input` to return fire request booleans. In `entities.py` (Rocket), implement `fire(all_sprites, missiles, assets)`: check cooldown (`constants.FIRE_COOLDOWN_MS`), calculate start position/velocity (use `constants.MISSILE_SPEED`), create `Missile` instance using `assets['missile']`, add to groups. In `physics.py`, implement `check_missile_despawn(missile, screen_rect)` to `kill()` missile if off-screen. In `main.py`, create `missiles` group. Handle fire requests from controls by calling `rocket.fire()`. In the update loop, iterate through `missiles`, calculate gravity for each, call `missile.update()`, and check despawn. For dev mode 8, players can fire missiles affected by gravity; missiles despawn correctly.

<br><br>

### Step 9: Collision System (`--dev-mode=9`)

* **Instruction:** Implement Step 9. In `physics.py`, implement `handle_collisions(rockets, missiles, celestial_bodies)`: Use `pygame.sprite.groupcollide` (with `collide_circle`) for Missile-Rocket (kill missile, apply `MISSILE_DAMAGE`, check owner), Rocket-Terrain (apply velocity-based damage using `COLLISION_DAMAGE_SCALE`, apply bounce), and Rocket-Rocket (apply velocity-based damage to both, apply bounce). Implement `calculate_bounce(velocity, normal, restitution)`. In `entities.py` (Rocket), implement `take_damage(amount)` updating `hp` and calling `self.explode()` if `hp <= 0`. Implement `explode()` to just `self.kill()` for now. Implement `reset(position)` method. In `ui.py`, implement `draw_hud` showing health bars (proportional rects) and scores. In `main.py`, call `physics.handle_collisions()` and `ui.draw_hud()`. For dev mode 9, collisions cause damage (visible on HUD) and bouncing; rockets disappear at 0 HP.

<br><br>

### Step 10: Game Flow & UI (`--dev-mode=10`)

* **Instruction:** Implement Step 10. In `main.py`, introduce game states (`playing`, `round_over`, `game_over`), round/score counters, timers. Manage state transitions based on rocket deaths and round count (`constants.MAX_ROUNDS`). Implement `start_new_round()` to reset/recreate rockets and clear missiles. In `game_state == 'round_over'` / `'game_over'`, display temporary messages using `ui.py` functions and check timers (`settings.ROUND_END_DELAY_MS`) before proceeding or quitting. In `ui.py`, implement `display_round_message` and `display_game_over_message`. Run the full game logic (input, physics, updates, collisions, drawing, state checks) within the appropriate game states. Call `start_new_round()` initially. For dev mode 10 (or normal run), the full game loop with rounds, scoring, temporary messages, and win/loss conditions should function.

<br><br>

### Step 11: Visual Polish & Tuning (`--dev-mode=11` or Normal Run)

* **Instruction:** Implement Step 11. In `entities.py`, modify `Rocket.explode()` and add `Missile.explode()`: Instead of `kill()`, change `self.image` to `assets['explosion']` (scale down 5x for missiles using `pygame.transform.scale`), set an explosion timer state. In `update`, if exploding, decrement timer; `kill()` when timer reaches zero. In `main.py`, load `assets['explosion']`. In `ui.py`, implement `draw_orbit_lines` using `pygame.draw.circle` for planets/moons based on their orbit parameters. Call this from `main.py`. Optionally implement rocket rotation in `Rocket.update` using `pygame.transform.rotate` based on velocity vector (ensure `self.orig_image` is stored). Review and tune values in `constants.py` for balanced gameplay. For dev mode 11 (or normal run), explosions are visible, orbit lines are drawn, rockets might rotate, and gameplay constants are tuned.

