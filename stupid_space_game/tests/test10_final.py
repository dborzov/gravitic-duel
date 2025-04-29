import pygame
import math
import time
from pygame.math import Vector2 # Import Vector2 directly for convenience

# --- Constants ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1440
TRIANGLE_COLOR = pygame.Color('yellow')
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

# Define Text Colors Globally
TEXT_COLOR = pygame.Color('white') # Default for initial side labels
RESULT_TEXT_COLOR = pygame.Color('cyan') # For side labels in final state
GUESS_VS_TRUE_COLOR = pygame.Color('lime') # For the guess/true comparison label
PROMPT_TEXT_COLOR = pygame.Color('lightgray') # For user prompts

# Global Font Variable (initialized after pygame.init)
GAME_FONT: pygame.font.Font = None

# --- Utility Functions ---
def clamp_rect_to_screen(rect: pygame.Rect, screen_width: int, screen_height: int) -> pygame.Rect:
    clamped_rect = rect.copy()
    clamped_rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))
    return clamped_rect

# --- Drawing Functions (Modified) ---

# Now uses Vector2, global font/colors
def draw_right_triangle_with_labels(
    screen: pygame.Surface,
    # font: pygame.font.Font, # Removed
    screen_width: int,
    screen_height: int,
    start_vec: Vector2, # Use Vector2
    target_vec: Vector2, # Use Vector2
    # text_color: pygame.Color = TEXT_COLOR # Removed, uses global TEXT_COLOR
) -> None:
    """Draws the basic triangle with side labels using Vector2 and global font."""
    if GAME_FONT is None: # Safety check
        print("ERROR: GAME_FONT not initialized!")
        return

    # --- 1. Calculate Geometry ---
    corner_vec = Vector2(target_vec.x, start_vec.y) # Corner using vector components
    delta_x = abs(start_vec.x - target_vec.x)
    delta_y = abs(start_vec.y - target_vec.y)

    # Convenience tuples for drawing functions
    start_pos_tuple = (int(start_vec.x), int(start_vec.y))
    target_pos_tuple = (int(target_vec.x), int(target_vec.y))
    corner_pos_tuple = (int(corner_vec.x), int(corner_vec.y))

    # --- 2. Draw the Triangle Components ---
    if delta_x > 0: pygame.draw.line(screen, TRIANGLE_COLOR, start_pos_tuple, corner_pos_tuple, LINE_WIDTH)
    if delta_y > 0: pygame.draw.line(screen, TRIANGLE_COLOR, corner_pos_tuple, target_pos_tuple, LINE_WIDTH)
    if delta_x > 0 or delta_y > 0: pygame.draw.line(screen, HYPOTENUSE_COLOR, start_pos_tuple, target_pos_tuple, HYPOTENUSE_LINE_WIDTH)

    # --- 3. Render, Position, Clamp, and Blit Labels (using global GAME_FONT, TEXT_COLOR) ---
    if delta_x >= MIN_LABEL_LENGTH:
        text_horiz_str = f"{delta_x:.0f}px" # Use .0f for cleaner int display
        text_horiz_surf = GAME_FONT.render(text_horiz_str, True, TEXT_COLOR)
        text_horiz_rect = text_horiz_surf.get_rect(centerx=int((start_vec.x + target_vec.x) / 2))
        # Position using vector components
        if target_vec.y <= start_vec.y: text_horiz_rect.top = int(start_vec.y + TEXT_PADDING)
        else: text_horiz_rect.bottom = int(start_vec.y - TEXT_PADDING)
        final_horiz_rect = clamp_rect_to_screen(text_horiz_rect, screen_width, screen_height)
        screen.blit(text_horiz_surf, final_horiz_rect)

    if delta_y >= MIN_LABEL_LENGTH:
        text_vert_str = f"{delta_y:.0f}px"
        text_vert_surf = GAME_FONT.render(text_vert_str, True, TEXT_COLOR)
        text_vert_rect = text_vert_surf.get_rect(centery=int((start_vec.y + target_vec.y) / 2))
        # Position using vector components
        if target_vec.x >= start_vec.x: text_vert_rect.left = int(target_vec.x + TEXT_PADDING)
        else: text_vert_rect.right = int(target_vec.x - TEXT_PADDING)
        final_vert_rect = clamp_rect_to_screen(text_vert_rect, screen_width, screen_height)
        screen.blit(text_vert_surf, final_vert_rect)


# Now uses Vector2
def animate_missile_and_explosion(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    start_vec: Vector2,    # Use Vector2
    target_vec: Vector2,   # Use Vector2
    players_guess: int
):
    """Animates missile flight and explosion using Vector2."""
    guessed_length_px = players_guess * 100.0
    # start_vec and target_vec are already vectors
    direction_vec = target_vec - start_vec
    true_length = direction_vec.length()

    if true_length < 0.01:
        print("Start/Target same, skipping animation.")
        pygame.time.wait(100)
        return

    unit_vec = direction_vec.normalize()

    # Convenience tuples for drawing functions (static points)
    start_pos_tuple = (int(start_vec.x), int(start_vec.y))
    target_pos_tuple = (int(target_vec.x), int(target_vec.y))
    corner_pos_tuple = (int(target_vec.x), int(start_vec.y)) # Recalculate tuple form

    # --- Phase 1: Missile Flight ---
    current_missile_length = 0.0
    while current_missile_length < guessed_length_px:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()

        elapsed_time_frame = dt
        current_missile_length += MISSILE_SPEED_PPT * (elapsed_time_frame / 1000.0)
        current_missile_length = min(current_missile_length, guessed_length_px)

        missile_end_vec = start_vec + unit_vec * current_missile_length
        missile_end_pos_tuple = (int(missile_end_vec.x), int(missile_end_vec.y)) # Tuple for drawing

        # Redraw basic scene for animation frame
        screen.fill(pygame.Color('black'))
        if abs(target_vec.x - start_vec.x) > 0: pygame.draw.line(screen, TRIANGLE_COLOR, start_pos_tuple, corner_pos_tuple, LINE_WIDTH)
        if abs(target_vec.y - start_vec.y) > 0: pygame.draw.line(screen, TRIANGLE_COLOR, corner_pos_tuple, target_pos_tuple, LINE_WIDTH)
        pygame.draw.line(screen, HYPOTENUSE_COLOR, start_pos_tuple, target_pos_tuple, HYPOTENUSE_LINE_WIDTH)
        pygame.draw.circle(screen, pygame.Color('pink'), start_pos_tuple, 10)
        pygame.draw.circle(screen, pygame.Color('pink'), target_pos_tuple, 10)
        if current_missile_length > 0.1: pygame.draw.line(screen, MISSILE_COLOR, start_pos_tuple, missile_end_pos_tuple, MISSILE_WIDTH)
        pygame.display.flip()
        if current_missile_length >= guessed_length_px: break

    explosion_center_vec = start_vec + unit_vec * guessed_length_px
    explosion_center_tuple = (int(explosion_center_vec.x), int(explosion_center_vec.y)) # Tuple for drawing

    # --- Phase 2: Explosion ---
    explosion_start_time = pygame.time.get_ticks()
    current_explosion_time = 0
    while current_explosion_time < EXPLOSION_DURATION_MS:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()

        current_explosion_time = pygame.time.get_ticks() - explosion_start_time
        progress = min(current_explosion_time / EXPLOSION_DURATION_MS, 1.0)
        radius_inner = progress * EXPLOSION_RADIUS_INNER_MAX
        radius_outer = progress * EXPLOSION_RADIUS_OUTER_MAX

        # Redraw basic scene for animation frame
        screen.fill(pygame.Color('black'))
        if abs(target_vec.x - start_vec.x) > 0: pygame.draw.line(screen, TRIANGLE_COLOR, start_pos_tuple, corner_pos_tuple, LINE_WIDTH)
        if abs(target_vec.y - start_vec.y) > 0: pygame.draw.line(screen, TRIANGLE_COLOR, corner_pos_tuple, target_pos_tuple, LINE_WIDTH)
        pygame.draw.line(screen, HYPOTENUSE_COLOR, start_pos_tuple, target_pos_tuple, HYPOTENUSE_LINE_WIDTH)
        pygame.draw.circle(screen, pygame.Color('pink'), start_pos_tuple, 10)
        pygame.draw.circle(screen, pygame.Color('pink'), target_pos_tuple, 10)
        # Use explosion_center_tuple for missile and circles
        if guessed_length_px > 0.1: pygame.draw.line(screen, MISSILE_COLOR, start_pos_tuple, explosion_center_tuple, MISSILE_WIDTH)
        if radius_outer > 0: pygame.draw.circle(screen, EXPLOSION_COLOR_OUTER, explosion_center_tuple, int(radius_outer), 0)
        if radius_inner > 0: pygame.draw.circle(screen, EXPLOSION_COLOR_INNER, explosion_center_tuple, int(radius_inner), 0)
        pygame.display.flip()


def draw_final_state(
    screen: pygame.Surface,
    # font: pygame.font.Font, # Removed
    screen_width: int,
    screen_height: int,
    start_vec: Vector2,       # Use Vector2
    target_vec: Vector2,      # Use Vector2
    players_guess: int
):
    """Draws final scene using Vector2 and global font/colors."""
    if GAME_FONT is None: # Safety check
        print("ERROR: GAME_FONT not initialized!")
        return

    # --- Calculations ---
    guessed_length_px = players_guess * 100.0
    # start_vec, target_vec already vectors
    direction_vec = target_vec - start_vec
    true_length = direction_vec.length()
    unit_vec = Vector2(0, 0)
    if true_length > 0.01: unit_vec = direction_vec.normalize()
    explosion_center_vec = start_vec + unit_vec * guessed_length_px

    # Tuples for drawing
    start_pos_tuple = (int(start_vec.x), int(start_vec.y))
    target_pos_tuple = (int(target_vec.x), int(target_vec.y))
    explosion_center_tuple = (int(explosion_center_vec.x), int(explosion_center_vec.y))

    # --- Drawing ---
    # 1. Base triangle, side labels (using RESULT_TEXT_COLOR now via global)
    #    Need to modify draw_right_triangle_with_labels to use RESULT_TEXT_COLOR internally
    #    OR pass color again OR handle it here. Let's handle it here by not calling it.
    #    Re-implement drawing needed elements directly:
    corner_vec = Vector2(target_vec.x, start_vec.y)
    corner_pos_tuple = (int(corner_vec.x), int(corner_vec.y))
    delta_x = abs(start_vec.x - target_vec.x)
    delta_y = abs(start_vec.y - target_vec.y)
    # Draw Legs/Hypotenuse
    if delta_x > 0: pygame.draw.line(screen, TRIANGLE_COLOR, start_pos_tuple, corner_pos_tuple, LINE_WIDTH)
    if delta_y > 0: pygame.draw.line(screen, TRIANGLE_COLOR, corner_pos_tuple, target_pos_tuple, LINE_WIDTH)
    if delta_x > 0 or delta_y > 0: pygame.draw.line(screen, HYPOTENUSE_COLOR, start_pos_tuple, target_pos_tuple, HYPOTENUSE_LINE_WIDTH)
    # Draw Side Labels (using RESULT_TEXT_COLOR)
    if delta_x >= MIN_LABEL_LENGTH:
        text_horiz_str = f"{delta_x:.0f}px"
        text_horiz_surf = GAME_FONT.render(text_horiz_str, True, RESULT_TEXT_COLOR) # Use result color
        text_horiz_rect = text_horiz_surf.get_rect(centerx=int((start_vec.x + target_vec.x) / 2))
        if target_vec.y <= start_vec.y: text_horiz_rect.top = int(start_vec.y + TEXT_PADDING)
        else: text_horiz_rect.bottom = int(start_vec.y - TEXT_PADDING)
        final_horiz_rect = clamp_rect_to_screen(text_horiz_rect, screen_width, screen_height)
        screen.blit(text_horiz_surf, final_horiz_rect)
    if delta_y >= MIN_LABEL_LENGTH:
        text_vert_str = f"{delta_y:.0f}px"
        text_vert_surf = GAME_FONT.render(text_vert_str, True, RESULT_TEXT_COLOR) # Use result color
        text_vert_rect = text_vert_surf.get_rect(centery=int((start_vec.y + target_vec.y) / 2))
        if target_vec.x >= start_vec.x: text_vert_rect.left = int(target_vec.x + TEXT_PADDING)
        else: text_vert_rect.right = int(target_vec.x - TEXT_PADDING)
        final_vert_rect = clamp_rect_to_screen(text_vert_rect, screen_width, screen_height)
        screen.blit(text_vert_surf, final_vert_rect)

    # 2. Start/target points
    pygame.draw.circle(screen, pygame.Color('pink'), start_pos_tuple, 10)
    pygame.draw.circle(screen, pygame.Color('pink'), target_pos_tuple, 10)

    # 3. Final missile line
    if guessed_length_px > 0.1:
        pygame.draw.line(screen, MISSILE_COLOR, start_pos_tuple, explosion_center_tuple, MISSILE_WIDTH)

    # 4. Final explosion state
    pygame.draw.circle(screen, EXPLOSION_COLOR_OUTER, explosion_center_tuple, EXPLOSION_RADIUS_OUTER_MAX, 0)
    pygame.draw.circle(screen, EXPLOSION_COLOR_INNER, explosion_center_tuple, EXPLOSION_RADIUS_INNER_MAX, 0)

    # 5. "Guess vs. True" label (using global GAME_FONT, GUESS_VS_TRUE_COLOR)
    guess_vs_true_text = f"Guess: {guessed_length_px:.0f}px | True: {true_length:.1f}px"
    guess_vs_true_surf = GAME_FONT.render(guess_vs_true_text, True, GUESS_VS_TRUE_COLOR)
    label_rect = guess_vs_true_surf.get_rect(centerx=explosion_center_tuple[0],
                                             bottom=explosion_center_tuple[1] - EXPLOSION_RADIUS_OUTER_MAX - TEXT_PADDING)
    if label_rect.top < TEXT_PADDING:
        label_rect.top = explosion_center_tuple[1] + EXPLOSION_RADIUS_OUTER_MAX + TEXT_PADDING
    final_label_rect = clamp_rect_to_screen(label_rect, screen_width, screen_height)
    screen.blit(guess_vs_true_surf, final_label_rect)


# --- Example Usage (Main Loop using Vector2 and globals) ---
if __name__ == '__main__':
    pygame.init()

    # --- Initialize Font AFTER pygame.init() and store globally ---
    try:
        print("Attempting to load system font 'dejavusansmono'...")
        GAME_FONT = pygame.font.SysFont('dejavusansmono', FONT_SIZE)
        print("System font loaded successfully.")
    except pygame.error as e:
        print(f"Warning: Could not load system font ('dejavusansmono'): {e}")
        # ... (rest of font loading fallback logic - unchanged) ...
        try:
             print("Attempting to load system font 'monospace'...")
             GAME_FONT = pygame.font.SysFont('monospace', FONT_SIZE)
             print("System font 'monospace' loaded successfully.")
        except pygame.error as e2:
            print(f"Warning: Could not load system font ('monospace'): {e2}")
            try:
                print("Attempting to load Pygame default font...")
                GAME_FONT = pygame.font.Font(None, FONT_SIZE)
                print("Pygame default font loaded successfully.")
            except pygame.error as e3:
                print(f"CRITICAL: Failed to initialize ANY font: {e3}")
                pygame.quit()
                exit()
            except Exception as e_general:
                print(f"CRITICAL: An unexpected error occurred during font loading: {e_general}")
                pygame.quit()
                exit()

    if GAME_FONT is None: # Exit if font loading failed completely
         print("CRITICAL: Font initialization failed. Exiting.")
         pygame.quit()
         exit()


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pythagoras Game - Vector2 Refactor")
    clock = pygame.time.Clock()

    # --- Game State (using Vector2) ---
    start_vec = Vector2(SCREEN_WIDTH // 5, SCREEN_HEIGHT * 4 // 5)
    target_vec = Vector2(0,0) # Placeholder, set in setup
    players_guess_units = 0

    def setup_new_round():
        """Helper to set up points (as Vectors) and guess for a round."""
        global start_vec, target_vec, players_guess_units
        t_x = int(SCREEN_WIDTH * (0.2 + 0.6 * (time.time()*0.7 % 1.0)))
        t_y = int(SCREEN_HEIGHT* (0.2 + 0.6 * (time.time()*0.9 % 1.0)))
        temp_target_vec = Vector2(t_x, t_y)
        # Ensure target is not identical to start
        while temp_target_vec == start_vec:
             temp_target_vec.y = (temp_target_vec.y + 10) % SCREEN_HEIGHT
        target_vec = temp_target_vec # Assign the valid vector

        direction_vec = target_vec - start_vec
        true_hypot = direction_vec.length()
        simulated_guess_px = true_hypot * (0.5 + (time.time()*1.1 % 1.0))
        pgu = round(simulated_guess_px / 100.0)
        players_guess_units = max(0, pgu)

        print("-" * 20)
        print(f"New Round Setup:")
        print(f"Start: {start_vec}, Target: {target_vec}") # Vectors print nicely
        print(f"True hypotenuse: {true_hypot:.1f} px")
        print(f"Player's guess: {players_guess_units} (Simulating {players_guess_units*100} px)")
        print("-" * 20)

    setup_new_round()

    state = "SHOW_TRIANGLE"
    running = True

    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Example: Use mouse click to set target vector
            if event.type == pygame.MOUSEBUTTONDOWN and state == "SHOW_TRIANGLE":
                 if event.button == 1: # Left click
                     target_vec = Vector2(event.pos) # Convert tuple from event.pos
                     # Recalculate guess based on new target for demo
                     direction_vec = target_vec - start_vec
                     true_hypot = direction_vec.length()
                     simulated_guess_px = true_hypot * (0.5 + (time.time()*1.1 % 1.0))
                     pgu = round(simulated_guess_px / 100.0)
                     players_guess_units = max(0, pgu)
                     print(f"New Target set by click: {target_vec}")
                     print(f"Recalculated True: {true_hypot:.1f}px, New Guess: {players_guess_units} units")


            if event.type == pygame.KEYDOWN:
                 if state == "SHOW_TRIANGLE" and event.key == pygame.K_SPACE:
                     state = "ANIMATING"
                 elif state == "POST_ANIMATION" and event.key == pygame.K_r:
                     setup_new_round()
                     state = "SHOW_TRIANGLE"


        # --- Game Logic & Drawing based on State ---
        if state == "SHOW_TRIANGLE":
            screen.fill(pygame.Color('black'))
            # Draw initial triangle using vectors and global font
            draw_right_triangle_with_labels(screen, # No font/color arg
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            start_vec, target_vec) # Pass vectors
            # Draw circles using vector components as tuples
            pygame.draw.circle(screen, pygame.Color('pink'), (int(start_vec.x), int(start_vec.y)), 10)
            pygame.draw.circle(screen, pygame.Color('pink'), (int(target_vec.x), int(target_vec.y)), 10)

            prompt_surf = GAME_FONT.render("Click to set Target | SPACE to fire!", True, PROMPT_TEXT_COLOR)
            prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, FONT_SIZE))
            screen.blit(prompt_surf, prompt_rect)

            pygame.display.flip()
            clock.tick(30)

        elif state == "ANIMATING":
            animate_missile_and_explosion(
                screen, clock,
                start_vec, target_vec, # Pass vectors
                players_guess_units
            )
            state = "POST_ANIMATION"

        elif state == "POST_ANIMATION":
            screen.fill(pygame.Color('black'))
            # Draw final state using vectors and global font
            draw_final_state(screen, # No font arg
                             start_vec, target_vec, # Pass vectors
                             players_guess_units)

            prompt_surf = GAME_FONT.render("Animation Complete. Press R to Reset.", True, PROMPT_TEXT_COLOR)
            prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, FONT_SIZE))
            screen.blit(prompt_surf, prompt_rect)

            pygame.display.flip()
            clock.tick(30)

    pygame.quit()
