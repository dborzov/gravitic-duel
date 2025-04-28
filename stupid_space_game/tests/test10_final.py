import pygame
import math
import time # For potential brief pauses - now maybe only for edge case

# --- Constants (Keep previous, add RESULT label color) ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1440
TRIANGLE_COLOR = pygame.Color('yellow')
TEXT_COLOR = pygame.Color('white') # For side labels
HYPOTENUSE_COLOR = pygame.Color('magenta') # Original hypotenuse path
LINE_WIDTH = 2
HYPOTENUSE_LINE_WIDTH = 4
FONT_SIZE = 24
TEXT_PADDING = 10
MIN_LABEL_LENGTH = 1

MISSILE_COLOR = pygame.Color('orange')
MISSILE_WIDTH = 6
MISSILE_SPEED_PPT = 5000 # Pixels Per Thousand ms

EXPLOSION_COLOR_INNER = pygame.Color('yellow')
EXPLOSION_COLOR_OUTER = pygame.Color('darkorange')
EXPLOSION_RADIUS_INNER_MAX = 50
EXPLOSION_RADIUS_OUTER_MAX = 100
EXPLOSION_DURATION_MS = 300

RESULT_TEXT_COLOR = pygame.Color('cyan') # For side lengths in final state
GUESS_VS_TRUE_COLOR = pygame.Color('lime') # For the new comparison label
# RESULT_PAUSE_DURATION_MS = 1500 # No longer needed in animation func

# --- Utility Functions (Keep clamp_rect_to_screen) ---
def clamp_rect_to_screen(rect: pygame.Rect, screen_width: int, screen_height: int) -> pygame.Rect:
    clamped_rect = rect.copy()
    clamped_rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))
    return clamped_rect

# --- Drawing Functions ---

# UNCHANGED: draw_right_triangle_with_labels
def draw_right_triangle_with_labels(
    screen: pygame.Surface,
    font: pygame.font.Font,
    screen_width: int,
    screen_height: int,
    x_start: int,
    y_start: int,
    x_target: int,
    y_target: int,
    text_color: pygame.Color = TEXT_COLOR # Allow overriding text color
) -> None:
    """Draws the basic triangle with side labels."""
    # ... (Code from previous version, unchanged internally) ...
    # ... (but added optional text_color argument) ...
    # --- 1. Calculate Geometry ---
    corner_x = x_target
    corner_y = y_start
    delta_x = abs(x_start - x_target)
    delta_y = abs(y_start - y_target)
    # --- 2. Draw the Triangle Components ---
    if delta_x > 0: pygame.draw.line(screen, TRIANGLE_COLOR, (x_start, y_start), (corner_x, corner_y), LINE_WIDTH)
    if delta_y > 0: pygame.draw.line(screen, TRIANGLE_COLOR, (corner_x, corner_y), (x_target, y_target), LINE_WIDTH)
    if delta_x > 0 or delta_y > 0: pygame.draw.line(screen, HYPOTENUSE_COLOR, (x_start, y_start), (x_target, y_target), HYPOTENUSE_LINE_WIDTH)
    # --- 3. Render, Position, Clamp, and Blit Labels ---
    if delta_x >= MIN_LABEL_LENGTH:
        text_horiz_str = f"{delta_x}px"
        text_horiz_surf = font.render(text_horiz_str, True, text_color) # Use text_color arg
        text_horiz_rect = text_horiz_surf.get_rect(centerx=(x_start + x_target) // 2)
        if y_target <= y_start: text_horiz_rect.top = y_start + TEXT_PADDING
        else: text_horiz_rect.bottom = y_start - TEXT_PADDING
        final_horiz_rect = clamp_rect_to_screen(text_horiz_rect, screen_width, screen_height)
        screen.blit(text_horiz_surf, final_horiz_rect)
    if delta_y >= MIN_LABEL_LENGTH:
        text_vert_str = f"{delta_y}px"
        text_vert_surf = font.render(text_vert_str, True, text_color) # Use text_color arg
        text_vert_rect = text_vert_surf.get_rect(centery=(y_start + y_target) // 2)
        if x_target >= x_start: text_vert_rect.left = x_target + TEXT_PADDING
        else: text_vert_rect.right = x_target - TEXT_PADDING
        final_vert_rect = clamp_rect_to_screen(text_vert_rect, screen_width, screen_height)
        screen.blit(text_vert_surf, final_vert_rect)


# MODIFIED: animate_missile_and_explosion (simpler, no final draw/pause)
def animate_missile_and_explosion(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    # font: pygame.font.Font, # No longer needed here
    # screen_width: int,     # No longer needed here
    # screen_height: int,    # No longer needed here
    start_pos: tuple[int, int],
    target_pos: tuple[int, int],
    players_guess: int
):
    """Animates missile flight and explosion. Does NOT draw final state."""
    x_start, y_start = start_pos
    x_target, y_target = target_pos
    guessed_length_px = players_guess * 100.0
    start_vec = pygame.math.Vector2(start_pos)
    target_vec = pygame.math.Vector2(target_pos)
    direction_vec = target_vec - start_vec
    true_length = direction_vec.length()

    if true_length < 0.01:
        print("Start/Target same, skipping animation.")
        # Need a small pause even here if skipping, otherwise feels instant
        pygame.time.wait(100)
        return # Exit early

    unit_vec = direction_vec.normalize()

    # --- Phase 1: Missile Flight ---
    current_missile_length = 0.0
    while current_missile_length < guessed_length_px:
        dt = clock.tick(60)
        for event in pygame.event.get(): # Essential event handling
            if event.type == pygame.QUIT: pygame.quit(); exit()

        elapsed_time_frame = dt
        current_missile_length += MISSILE_SPEED_PPT * (elapsed_time_frame / 1000.0)
        current_missile_length = min(current_missile_length, guessed_length_px)
        missile_end_vec = start_vec + unit_vec * current_missile_length
        missile_end_pos = (int(missile_end_vec.x), int(missile_end_vec.y))

        # Redraw basic scene for animation frame
        screen.fill(pygame.Color('black'))
        if abs(x_target - x_start) > 0: pygame.draw.line(screen, TRIANGLE_COLOR, start_pos, (x_target, y_start), LINE_WIDTH)
        if abs(y_target - y_start) > 0: pygame.draw.line(screen, TRIANGLE_COLOR, (x_target, y_start), target_pos, LINE_WIDTH)
        pygame.draw.line(screen, HYPOTENUSE_COLOR, start_pos, target_pos, HYPOTENUSE_LINE_WIDTH)
        pygame.draw.circle(screen, pygame.Color('pink'), start_pos, 10)
        pygame.draw.circle(screen, pygame.Color('pink'), target_pos, 10)
        if current_missile_length > 0.1: pygame.draw.line(screen, MISSILE_COLOR, start_pos, missile_end_pos, MISSILE_WIDTH)
        pygame.display.flip()
        if current_missile_length >= guessed_length_px: break

    explosion_center_vec = start_vec + unit_vec * guessed_length_px
    explosion_center = (int(explosion_center_vec.x), int(explosion_center_vec.y))

    # --- Phase 2: Explosion ---
    explosion_start_time = pygame.time.get_ticks()
    current_explosion_time = 0
    while current_explosion_time < EXPLOSION_DURATION_MS:
        dt = clock.tick(60)
        for event in pygame.event.get(): # Essential event handling
            if event.type == pygame.QUIT: pygame.quit(); exit()

        current_explosion_time = pygame.time.get_ticks() - explosion_start_time
        progress = min(current_explosion_time / EXPLOSION_DURATION_MS, 1.0)
        radius_inner = progress * EXPLOSION_RADIUS_INNER_MAX
        radius_outer = progress * EXPLOSION_RADIUS_OUTER_MAX

        # Redraw basic scene for animation frame
        screen.fill(pygame.Color('black'))
        if abs(x_target - x_start) > 0: pygame.draw.line(screen, TRIANGLE_COLOR, start_pos, (x_target, y_start), LINE_WIDTH)
        if abs(y_target - y_start) > 0: pygame.draw.line(screen, TRIANGLE_COLOR, (x_target, y_start), target_pos, LINE_WIDTH)
        pygame.draw.line(screen, HYPOTENUSE_COLOR, start_pos, target_pos, HYPOTENUSE_LINE_WIDTH)
        pygame.draw.circle(screen, pygame.Color('pink'), start_pos, 10)
        pygame.draw.circle(screen, pygame.Color('pink'), target_pos, 10)
        if guessed_length_px > 0.1: pygame.draw.line(screen, MISSILE_COLOR, start_pos, explosion_center, MISSILE_WIDTH) # Final missile line
        if radius_outer > 0: pygame.draw.circle(screen, EXPLOSION_COLOR_OUTER, explosion_center, int(radius_outer), 0)
        if radius_inner > 0: pygame.draw.circle(screen, EXPLOSION_COLOR_INNER, explosion_center, int(radius_inner), 0)
        pygame.display.flip()
    # Animation function now simply finishes after the explosion loop.


# --- NEW Final State Drawing Function ---
def draw_final_state(
    screen: pygame.Surface,
    font: pygame.font.Font,
    screen_width: int,
    screen_height: int,
    start_pos: tuple[int, int],
    target_pos: tuple[int, int],
    players_guess: int # Guess in units of 100px
):
    """
    Draws the complete final scene after animation: triangle, side labels,
    missile line, explosion, and guess vs true length label.
    Assumes background is already filled.
    """
    x_start, y_start = start_pos
    x_target, y_target = target_pos

    # --- Calculations (needed for drawing elements) ---
    guessed_length_px = players_guess * 100.0
    start_vec = pygame.math.Vector2(start_pos)
    target_vec = pygame.math.Vector2(target_pos)
    direction_vec = target_vec - start_vec
    true_length = direction_vec.length()

    # Avoid division by zero if start == target
    unit_vec = pygame.math.Vector2(0, 0)
    if true_length > 0.01:
        unit_vec = direction_vec.normalize()

    explosion_center_vec = start_vec + unit_vec * guessed_length_px
    explosion_center = (int(explosion_center_vec.x), int(explosion_center_vec.y))

    # --- Drawing ---
    # 1. Draw base triangle, side labels, original hypotenuse path
    #    Using a different color for side labels in final state for contrast
    draw_right_triangle_with_labels(screen, font, screen_width, screen_height,
                                    x_start, y_start, x_target, y_target,
                                    text_color=RESULT_TEXT_COLOR) # Use cyan for side labels now

    # 2. Draw start/target points (optional, but good for context)
    pygame.draw.circle(screen, pygame.Color('pink'), start_pos, 10)
    pygame.draw.circle(screen, pygame.Color('pink'), target_pos, 10)

    # 3. Draw the final missile line (from start to explosion)
    #    Only draw if guess was non-zero to avoid dot at start
    if guessed_length_px > 0.1:
        pygame.draw.line(screen, MISSILE_COLOR, start_pos, explosion_center, MISSILE_WIDTH)

    # 4. Draw the final explosion state (max radius)
    pygame.draw.circle(screen, EXPLOSION_COLOR_OUTER, explosion_center, EXPLOSION_RADIUS_OUTER_MAX, 0)
    pygame.draw.circle(screen, EXPLOSION_COLOR_INNER, explosion_center, EXPLOSION_RADIUS_INNER_MAX, 0)

    # 5. Prepare and draw the "Guess vs. True" label near the explosion
    guess_vs_true_text = f"Guess: {guessed_length_px:.0f}px | True: {true_length:.1f}px"
    guess_vs_true_surf = font.render(guess_vs_true_text, True, GUESS_VS_TRUE_COLOR)

    # Position the label relative to the explosion center
    # Try placing it just above the outer explosion radius
    label_rect = guess_vs_true_surf.get_rect(centerx=explosion_center[0],
                                             bottom=explosion_center[1] - EXPLOSION_RADIUS_OUTER_MAX - TEXT_PADDING)

    # Adjust if it goes off screen top/bottom primarily
    if label_rect.top < TEXT_PADDING: # If too high, move below explosion
        label_rect.top = explosion_center[1] + EXPLOSION_RADIUS_OUTER_MAX + TEXT_PADDING
    # Clamp horizontally too
    final_label_rect = clamp_rect_to_screen(label_rect, screen_width, screen_height)

    screen.blit(guess_vs_true_surf, final_label_rect)


# --- Example Usage (Main Loop using the new structure) ---
if __name__ == '__main__':
    pygame.init()

    # --- Font Loading ---
    game_font = None
    try:
        # ... (font loading code - unchanged) ...
        print("Attempting to load system font 'dejavusansmono'...")
        game_font = pygame.font.SysFont('dejavusansmono', FONT_SIZE)
        print("System font loaded successfully.")
    except pygame.error as e:
        print(f"Warning: Could not load system font ('dejavusansmono'): {e}")
        try:
             print("Attempting to load system font 'monospace'...")
             game_font = pygame.font.SysFont('monospace', FONT_SIZE)
             print("System font 'monospace' loaded successfully.")
        except pygame.error as e2:
            print(f"Warning: Could not load system font ('monospace'): {e2}")
            try:
                print("Attempting to load Pygame default font...")
                game_font = pygame.font.Font(None, FONT_SIZE)
                print("Pygame default font loaded successfully.")
            except pygame.error as e3:
                print(f"CRITICAL: Failed to initialize ANY font: {e3}")
                pygame.quit()
                exit()
            except Exception as e_general:
                print(f"CRITICAL: An unexpected error occurred during font loading: {e_general}")
                pygame.quit()
                exit()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pythagoras Game - Final State Test")
    clock = pygame.time.Clock()

    # --- Game State ---
    start_pos = (SCREEN_WIDTH // 5, SCREEN_HEIGHT * 4 // 5)
    target_pos = (SCREEN_WIDTH * 4 // 5, SCREEN_HEIGHT // 5)
    players_guess_units = 0 # Initialize

    def setup_new_round():
        """Helper to set up points and guess for a round."""
        global start_pos, target_pos, players_guess_units # Modify global state
        # Keep start pos, randomize target
        t_x = int(SCREEN_WIDTH * (0.2 + 0.6 * (time.time()*0.7 % 1.0)))
        t_y = int(SCREEN_HEIGHT* (0.2 + 0.6 * (time.time()*0.9 % 1.0)))
        # Ensure target is not identical to start
        while (t_x, t_y) == start_pos:
             t_y = (t_y + 10) % SCREEN_HEIGHT
        target_pos = (t_x, t_y)

        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        true_hypot = math.hypot(dx, dy)
        # Simulate a guess between 50% and 150% of true length
        simulated_guess_px = true_hypot * (0.5 + (time.time()*1.1 % 1.0))
        pgu = round(simulated_guess_px / 100.0)
        # Ensure guess is at least 0
        players_guess_units = max(0, pgu)

        print("-" * 20)
        print(f"New Round Setup:")
        print(f"Start: {start_pos}, Target: {target_pos}")
        print(f"True hypotenuse: {true_hypot:.1f} px")
        print(f"Player's guess: {players_guess_units} (Simulating {players_guess_units*100} px)")
        print("-" * 20)

    setup_new_round() # Initial setup

    state = "SHOW_TRIANGLE"
    running = True

    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                 if state == "SHOW_TRIANGLE" and event.key == pygame.K_SPACE:
                     state = "ANIMATING"
                 elif state == "POST_ANIMATION" and event.key == pygame.K_r:
                     setup_new_round()
                     state = "SHOW_TRIANGLE"


        # --- Game Logic & Drawing based on State ---
        if state == "SHOW_TRIANGLE":
            screen.fill(pygame.Color('black'))
            # Draw the initial triangle with standard white labels
            draw_right_triangle_with_labels(screen, game_font,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            start_pos[0], start_pos[1],
                                            target_pos[0], target_pos[1])
            pygame.draw.circle(screen, pygame.Color('pink'), start_pos, 10)
            pygame.draw.circle(screen, pygame.Color('pink'), target_pos, 10)

            prompt_surf = game_font.render("Press SPACE to fire missile!", True, TEXT_COLOR)
            prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, FONT_SIZE))
            screen.blit(prompt_surf, prompt_rect)

            pygame.display.flip()
            clock.tick(30)

        elif state == "ANIMATING":
            # Animation function takes over temporarily
            animate_missile_and_explosion(
                screen, clock,
                # font, screen_width, screen_height, # No longer needed args
                start_pos, target_pos,
                players_guess_units
            )
            state = "POST_ANIMATION" # Move to next state after animation returns

        elif state == "POST_ANIMATION":
            # This state now repeatedly draws the final scene using the new function
            screen.fill(pygame.Color('black'))

            # Call the dedicated function to draw the final state
            draw_final_state(screen, game_font,
                             SCREEN_WIDTH, SCREEN_HEIGHT,
                             start_pos, target_pos,
                             players_guess_units)

            # Add prompt overlay
            prompt_surf = game_font.render("Animation Complete. Press R to Reset.", True, TEXT_COLOR)
            prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, FONT_SIZE))
            screen.blit(prompt_surf, prompt_rect)

            pygame.display.flip()
            clock.tick(30) # Keep CPU usage reasonable in static state


    pygame.quit()
