# Gravitic Duel - Development Mode Descriptions (DEV_MODES.md)

This document describes the expected behavior and testing criteria for each `--dev-mode=N` command-line argument when running `main.py`.

---

* **Command:** `python3 gravitic_duel/main.py --dev-mode=1`
    * **Expected View:** A fullscreen (2560x1440) black window. A static text message (e.g., "DEV MODE 1 ACTIVE") is displayed, centered.
    * **Interaction:** Pressing `ESC` or closing the window quits the application cleanly. No other interaction.

<br><br>

* **Command:** `python3 gravitic_duel/main.py --dev-mode=2`
    * **Expected View:** A fullscreen window displaying the static `background.png` image.
    * **Interaction:** Pressing `ESC` or closing the window quits. No other interaction.

<br><br>

* **Command:** `python3 gravitic_duel/main.py --dev-mode=3`
    * **Expected View:** The space background is displayed. The `star.png` sprite is visible (likely centered). Several static colored circles representing the planets and smaller static colored circles representing moons are visible at their calculated initial orbital positions.
    * **Interaction:** Pressing `ESC` or closing the window quits. No other interaction.

<br><br>

* **Command:** `python3 gravitic_duel/main.py --dev-mode=4`
    * **Expected View:** The space background and star sprite are visible. The colored circles representing planets orbit the star. The smaller colored circles representing moons orbit their respective planets. Movement should appear smooth.
    * **Interaction:** Pressing `ESC` or closing the window quits. No other interaction.

<br><br>

* **Command:** `python3 gravitic_duel/main.py --dev-mode=5`
    * **Expected View:** Background, orbiting star/planets/moons are visible. Two static `rocket.png` sprites are visible at their designated starting positions.
    * **Interaction:** Pressing `ESC` or closing the window quits. No other interaction.

<br><br>

* **Command:** `python3 gravitic_duel/main.py --dev-mode=6`
    * **Expected View:** Background, orbiting bodies, and two rockets are visible.
    * **Interaction:** Pressing `W/A/S/D` applies thrust to Player 1's rocket, causing it to accelerate and move with inertia. Pressing `Numpad 8/4/2/6` applies thrust to Player 2's rocket similarly. Pressing `ESC` quits.

<br><br>

* **Command:** `python3 gravitic_duel/main.py --dev-mode=7`
    * **Expected View:** Background, orbiting bodies, and two controllable rockets are visible.
    * **Interaction:** Rockets behave as in Mode 6, but their trajectories are now influenced by the gravitational pull of the star and planets. When a rocket flies off one screen edge, it reappears on the opposite edge, maintaining its velocity. Pressing `ESC` quits.

<br><br>

* **Command:** `python3 gravitic_duel/main.py --dev-mode=8`
    * **Expected View:** Background, orbiting bodies, controllable rockets affected by gravity and screen wrap.
    * **Interaction:** Players can press `Q` (P1) or `Numpad 7` (P2) to fire `missile.png` sprites. Firing respects a cooldown. Missiles inherit rocket velocity plus a forward boost, are affected by gravity, disappear after 30 seconds, and are destroyed if they hit a screen edge. Pressing `ESC` quits.

<br><br>

* **Command:** `python3 gravitic_duel/main.py --dev-mode=9`
    * **Expected View:** Full environment as in Mode 8. Additionally, a HUD is visible at the top: Health bars for P1 (left) and P2 (right), and a score display (center, initially 0-0).
    * **Interaction:** All previous interactions work. Collisions now have consequences: Missiles hitting opponents reduce HP (visible on HUD) and destroy the missile. Rockets hitting planets/moons/star reduce HP, cause bounce. Rockets hitting each other reduce both HP, cause bounce. When HP reaches zero, the rocket sprite disappears. Pressing `ESC` quits.

<br><br>

* **Command:** `python3 gravitic_duel/main.py --dev-mode=10` (or `python3 gravitic_duel/main.py`)
    * **Expected View:** Full game environment with HUD.
    * **Interaction:** Full game flow is active. When a player's rocket is destroyed, the round ends, the score updates, a "PLAYER X WINS ROUND!" message appears for ~3 seconds. The next round starts automatically with rockets reset. After 5 rounds, a "PLAYER X WINS GAME!" message appears for ~3 seconds, and the game automatically quits. Ties are handled. Pressing `ESC` quits immediately.

<br><br>

* **Command:** `python3 gravitic_duel/main.py --dev-mode=11` (or `python3 gravitic_duel/main.py`)
    * **Expected View:** Full game environment as in Mode 10. Additionally, faint circular lines indicating planet/moon orbits are visible. When rockets or missiles are destroyed, the `explosion.png` sprite appears briefly at their location (scaled down ~5x for missiles). Rockets may optionally rotate to face their direction of travel.
    * **Interaction:** Full game flow as in Mode 10. Gameplay balance (speed, damage, gravity) should feel intentional due to tuning in `constants.py`. Pressing `ESC` quits.

