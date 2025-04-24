# Gravitic Duel - Game Specification (SPEC.md)

**Version:** 1.0
**Date:** 2025-04-22

## 1. Overview & Concept

* **Genre:** 2D Multiplayer Space Combat Arena
* **Engine:** Pygame (Python 3)
* **Target Platform:** Ubuntu Linux (GNOME DE assumed, should be cross-platform)
* **Core Concept:** A two-player, local-multiplayer game set in a 2D "solar system" view. Control is via directional thrusters. Players duel using missiles in a best-of-5-rounds format.
* **Visual Style:** Pixel art sprites:  rockets, the star, missiles, explosions.


## 2. Core Gameplay Mechanics

* **Multiplayer:** 2 players on a single computer, sharing one screen.
* **Physics:**
    * Newtonian Motion: Rockets and missiles operate under inertia.
    * Gravity: A central star and 5 orbiting planets exert gravitational pull on rockets and missiles (inverse square law approximation). Moons exert negligible/zero gravity.
    * Thrust Control: Player input activates directional thrusters (Up/Down/Left/Right world axes), applying constant acceleration to modify the rocket's velocity vector.
    * Screen Behavior: Rockets wrap screen edges. Missiles are destroyed at screen edges. Planets/Moons move according to orbits and can go off-screen (ceasing interaction while off-screen).
* **Combat:**
    * Missiles: Fired via player key (`Q`/`Numpad 7`). Subject to physics.
    * Cooldown: 2-3 second firing cooldown per player.
    * Missile Lifetime: Max 30 seconds. Destroyed on impact (rocket, planet, moon, star), at screen edge, or timeout.
* **Health & Damage:**
    * HP: Each rocket has health points (HP), displayed via top-screen bars.
    * Damage Sources: Opponent's missile hit (fixed damage), collision with planets/moons/star (damage proportional to relative impact velocity), collision with opponent rocket (damage proportional to relative impact velocity).
    * Destruction: HP <= 0 triggers explosion visual (shared explosion sprite, scaled down for missiles) and removal after a short delay. Can result in a round tie.
* **Win Condition:** Best of 5 rounds. Player with the most round wins after 5 rounds wins the game.


## 3. Entities

* **Player Rockets (x2):** Controlled by players. Subject to physics. Fire missiles. Have HP. Collide with terrain, missiles, other rocket. Visually represented by `rocket.png`, potentially color-tinted per player.
* **Missiles:** Fired by rockets. Subject to physics. Limited lifetime. Cause damage. Visually represented by `missile.png`. Use scaled-down `explosion.png` on destruction.
* **Central Star (x1):** Stationary. Primary gravity source. Destructive collision. Visually represented by `star.png`.
* **Planets (x5):** Orbit star (circular paths). Secondary gravity sources. Cause collision damage. Drawn as simple colored circles of varying sizes. Orbit paths visually hinted at.
* **Moons (~10 total):** Orbit respective planets (circular paths). Negligible/zero gravity. Cause collision damage. Drawn as small, simple colored circles. Orbit paths visually hinted at.


## 4. Physics Details (Conceptual)

* **Integration:** Simple Euler integration for position/velocity updates based on total acceleration (thrust + gravity).
* **Gravity:** Calculated from star and on-screen planets using inverse square law ($F \propto \frac{M_{source}}{|\vec{r}|^2}$), scaled by `GRAVITY_FACTOR`. `mass_proxy` used for M. Clamped at minimum distance.
* **Thrust:** Constant acceleration vector applied along world axes when key is held.
* **Collisions:** Circle-based collision detection (`pygame.sprite.collide_circle`).
* **Response:** Damage application based on source. Bouncing uses velocity reflection based on collision normal and a restitution factor (`BOUNCE_FACTOR`).


## 5. Controls

* **Player 1:** `W/A/S/D` (Up/Left/Down/Right thrust), `Q` (Fire).
* **Player 2:** `Numpad 8/4/2/6` (Up/Left/Down/Right thrust), `Numpad 7` (Fire).
* **Global:** `ESC` (Quit game).


## 6. User Interface (UI)

* **Screen:** 2560x1440 resolution, fullscreen/windowless.
* **HUD:** Top-left: P1 Health Bar. Top-right: P2 Health Bar. Top-center: Score ("P1: [Score] - P2: [Score]").
* **Messages:** Large centered text overlay for round end ("PLAYER X WINS ROUND!", "ROUND TIED!") and game end ("PLAYER X WINS GAME!", "GAME TIED!"). Displayed temporarily.
* **Visuals:** Static space background image. Faded lines indicating orbits.


## 7. Game Flow

1.  **Launch:** Game starts immediately in Round 1 (Score 0-0). Rockets spawn.
2.  **Round Play:** Players control rockets, shoot, navigate. Physics simulation runs. Round ends when one or both rockets are destroyed.
3.  **Round End:** Update score. Display round winner message (3 seconds).
4.  **Next Round:** If < 5 rounds played, reset rockets/missiles, start next round.
5.  **Game End:** After Round 5, display final game winner message (3 seconds).
6.  **Exit:** Game exits automatically after final message or when `ESC` is pressed.



