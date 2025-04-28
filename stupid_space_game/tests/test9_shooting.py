import pygame
import math
import time # For potential brief pauses

# --- Constants (Adjust as needed) ---
# Screen/Existing Geometry Constants (assuming they are defined globally or passed)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1440
TRIANGLE_COLOR = pygame.Color('yellow')
TEXT_COLOR = pygame.Color('white')
HYPOTENUSE_COLOR = pygame.Color('magenta')
LINE_WIDTH = 2
HYPOTENUSE_LINE_WIDTH = 4
FONT_SIZE = 24
TEXT_PADDING = 10
MIN_LABEL_LENGTH = 1

# --- NEW Animation Constants ---
MISSILE_COLOR = pygame.Color('orange')
MISSILE_WIDTH = 6 # Thick line for the missile
MISSILE_SPEED_PPT = 5000 # Speed in Pixels Per Thousand ms (adjust for desired speed)

EXPLOSION_COLOR_INNER = pygame.Color('yellow')
EXPLOSION_COLOR_OUTER = pygame.Color('darkorange')
EXPLOSION_RADIUS_INNER_MAX = 50
EXPLOSION_RADIUS_OUTER_MAX = 100
EXPLOSION_DURATION_MS = 300 # Milliseconds for explosion expansion

RESULT_TEXT_COLOR = pygame.Color('cyan')
RESULT_PAUSE_DURATION_MS = 1500 # Hold result screen for this long before returning

# --- Function Definitions (Keep previous ones) ---

def clamp_rect_to_screen(rect: pygame.Rect, screen_width: int, screen_height: int) -> pygame.Rect:
    # ... (keep the clamp_rect_to_screen function from previous step) ...
    clamped_rect = rect.copy()
    clamped_rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))
    return clamped_rect

def draw_right_triangle_with_labels(
    screen: pygame.Surface,
    font: pygame.font.Font,
    screen_width: int,
    screen_height: int,
    x_start: int,
    y_start: int,
    x_target: int,
    y_target: int
) -> None:
    # ... (keep the draw_right_triangle_with_labels function from previous step) ...
    # --- 1. Calculate Geometry ---
    corner_x = x_target
    corner_y = y_start
    delta_x = abs(x_target - x_start)
    delta_y = abs(y_target - y_start)

    # --- 2. Draw the Triangle Components ---
    if delta_x > 0:
        pygame.draw.line(screen, TRIANGLE_COLOR, (x_start, y_start), (corner_x, corner_y), LINE_WIDTH)
    if delta_y > 0:
        pygame.draw.line(screen, TRIANGLE_COLOR, (corner_x, corner_y), (x_target, y_target), LINE_WIDTH)
    if delta_x > 0 or delta_y > 0:
        pygame.draw.line(screen, HYPOTENUSE_COLOR, (x_start, y_start), (x_target, y_target), HYPOTENUSE_LINE_WIDTH)

    # --- 3. Render, Position, Clamp, and Blit Labels ---
    # Horizontal Label
    if delta_x >= MIN_LABEL_LENGTH:
        text_horiz_str = f"{delta_x}px"
        text_horiz_surf = font.render(text_horiz_str, True, TEXT_COLOR)
        text_horiz_rect = text_horiz_surf.get_rect(centerx=(x_start + x_target) // 2)
        if y_target <= y_start: text_horiz_rect.top = y_start + TEXT_PADDING
        else: text_horiz_rect.bottom = y_start - TEXT_PADDING
        final_horiz_rect = clamp_rect_to_screen(text_horiz_rect, screen_width, screen_height)
        screen.blit(text_horiz_surf, final_horiz_rect)
    # Vertical Label
    if delta_y >= MIN_LABEL_LENGTH:
        text_vert_str = f"{delta_y}px"
        text_vert_surf = font.render(text_vert_str, True, TEXT_COLOR)
        text_vert_rect = text_vert_surf.get_rect(centery=(y_start + y_target) // 2)
        if x_target >= x_start: text_vert_rect.left = x_target + TEXT_PADDING
        else: text_vert_rect.right = x_target - TEXT_PADDING
        final_vert_rect = clamp_rect_to_screen(text_vert_rect, screen_width, screen_height)
        screen.blit(text_vert_surf, final_vert_rect)


# --- NEW Animation Function ---
def animate_missile_and_explosion(
    screen: pygame.Surface,
    clock: pygame.time.Clock, # Pass the game clock
    font: pygame.font.Font,   # Font for result label
    screen_width: int,
    screen_height: int,
    start_pos: tuple[int, int],
    target_pos: tuple[int, int],
    players_guess: int # Guess in units of 100px
):
    """
    Animates a missile flight based on player's guess, an explosion,
    and displays the true hypotenuse length.
    """
    x_start, y_start = start_pos
    x_target, y_target = target_pos

    # --- Calculations ---
    guessed_length_px = players_guess * 100.0 # Use float for precision
    start_vec = pygame.math.Vector2(start_pos)
    target_vec = pygame.math.Vector2(target_pos)
    direction_vec = target_vec - start_vec

    true_length = direction_vec.length()

    # Handle edge case: start == target
    if true_length < 0.01: # Use a small epsilon for float comparison
        print("Start and target points are the same. Skipping animation.")
        # Optionally display a message or just return
        # Display true length (0) briefly
        result_text = f"True Distance: {true_length:.1f}px"
        result_surf = font.render(result_text, True, RESULT_TEXT_COLOR)
        result_rect = result_surf.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.fill(pygame.Color('black'))
        screen.blit(result_surf, result_rect)
        pygame.display.flip()
        pygame.time.wait(RESULT_PAUSE_DURATION_MS) # Wait using pygame time
        return

    unit_vec = direction_vec.normalize()

    # --- Phase 1: Missile Flight Animation ---
    current_missile_length = 0.0
    missile_start_time = pygame.time.get_ticks() # Time in milliseconds

    running_animation = True
    while running_animation and current_missile_length < guessed_length_px:
        dt = clock.tick(20) # Get delta time in ms, limit FPS

        # Essential: Handle QUIT event during animation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit() # Consider a more graceful exit maybe
                 exit()

        # Update missile length based on time and speed
        elapsed_time_frame = dt # Use delta time from clock tick
        current_missile_length += MISSILE_SPEED_PPT * (elapsed_time_frame / 1000.0)

        # Clamp length to the guessed length
        current_missile_length = min(current_missile_length, guessed_length_px)

        # Calculate current missile end point
        missile_end_vec = start_vec + unit_vec * current_missile_length
        missile_end_pos = (int(missile_end_vec.x), int(missile_end_vec.y))

        # --- Redraw scene for this frame ---
        screen.fill(pygame.Color('black'))
        # Draw the static triangle elements WITHOUT labels (less clutter during animation)
        if abs(x_target - x_start) > 0:
            pygame.draw.line(screen, TRIANGLE_COLOR, start_pos, (x_target, y_start), LINE_WIDTH)
        if abs(y_target - y_start) > 0:
            pygame.draw.line(screen, TRIANGLE_COLOR, (x_target, y_start), target_pos, LINE_WIDTH)
        pygame.draw.line(screen, HYPOTENUSE_COLOR, start_pos, target_pos, HYPOTENUSE_LINE_WIDTH)
        # Draw start/target points
        pygame.draw.circle(screen, pygame.Color('pink'), start_pos, 10)
        pygame.draw.circle(screen, pygame.Color('pink'), target_pos, 10)


        # Draw the extending missile line
        # Ensure start/end are different before drawing line
        if current_missile_length > 0.1:
            pygame.draw.line(screen, MISSILE_COLOR, start_pos, missile_end_pos, MISSILE_WIDTH)

        pygame.display.flip()

        # Check if missile reached target length
        if current_missile_length >= guessed_length_px:
            break # Exit missile flight loop

    # Store final missile end point for explosion center
    final_missile_end_vec = start_vec + unit_vec * guessed_length_px
    explosion_center = (int(final_missile_end_vec.x), int(final_missile_end_vec.y))

    # --- Phase 2: Explosion Animation ---
    explosion_start_time = pygame.time.get_ticks()
    current_explosion_time = 0

    while current_explosion_time < EXPLOSION_DURATION_MS:
        dt = clock.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
                 exit()

        current_explosion_time = pygame.time.get_ticks() - explosion_start_time
        progress = min(current_explosion_time / EXPLOSION_DURATION_MS, 1.0) # Normalize progress 0 to 1

        # Calculate current radii based on progress
        radius_inner = progress * EXPLOSION_RADIUS_INNER_MAX
        radius_outer = progress * EXPLOSION_RADIUS_OUTER_MAX

        # --- Redraw scene for explosion frame ---
        screen.fill(pygame.Color('black'))
        # Draw static triangle elements
        if abs(x_target - x_start) > 0:
            pygame.draw.line(screen, TRIANGLE_COLOR, start_pos, (x_target, y_start), LINE_WIDTH)
        if abs(y_target - y_start) > 0:
            pygame.draw.line(screen, TRIANGLE_COLOR, (x_target, y_start), target_pos, LINE_WIDTH)
        pygame.draw.line(screen, HYPOTENUSE_COLOR, start_pos, target_pos, HYPOTENUSE_LINE_WIDTH)
        # Draw start/target points
        pygame.draw.circle(screen, pygame.Color('pink'), start_pos, 10)
        pygame.draw.circle(screen, pygame.Color('pink'), target_pos, 10)

        # Draw the final missile line (optional, could be covered by explosion)
        pygame.draw.line(screen, MISSILE_COLOR, start_pos, explosion_center, MISSILE_WIDTH)

        # Draw expanding explosion circles (filled)
        # Draw outer circle first so inner is on top
        if radius_outer > 0:
             pygame.draw.circle(screen, EXPLOSION_COLOR_OUTER, explosion_center, int(radius_outer), 0)
        if radius_inner > 0:
             pygame.draw.circle(screen, EXPLOSION_COLOR_INNER, explosion_center, int(radius_inner), 0)


        pygame.display.flip()

    # --- Phase 3: Show Result ---
    # Prepare result text
    result_text = f"True Distance: {true_length:.1f}px" # Rounded to 1 decimal place
    result_surf = font.render(result_text, True, RESULT_TEXT_COLOR)
    # Position the text (e.g., below the center or near the target)
    result_rect = result_surf.get_rect(center=(screen_width // 2, screen_height - FONT_SIZE * 2))


    # Final redraw showing result
    screen.fill(pygame.Color('black'))
    # Draw static triangle elements
    if abs(x_target - x_start) > 0:
        pygame.draw.line(screen, TRIANGLE_COLOR, start_pos, (x_target, y_start), LINE_WIDTH)
    if abs(y_target - y_start) > 0:
        pygame.draw.line(screen, TRIANGLE_COLOR, (x_target, y_start), target_pos, LINE_WIDTH)
    pygame.draw.line(screen, HYPOTENUSE_COLOR, start_pos, target_pos, HYPOTENUSE_LINE_WIDTH)
    # Draw start/target points
    pygame.draw.circle(screen, pygame.Color('pink'), start_pos, 10)
    pygame.draw.circle(screen, pygame.Color('pink'), target_pos, 10)
    # Draw final missile line
    pygame.draw.line(screen, MISSILE_COLOR, start_pos, explosion_center, MISSILE_WIDTH)
    # Draw final explosion state
    pygame.draw.circle(screen, EXPLOSION_COLOR_OUTER, explosion_center, EXPLOSION_RADIUS_OUTER_MAX, 0)
    pygame.draw.circle(screen, EXPLOSION_COLOR_INNER, explosion_center, EXPLOSION_RADIUS_INNER_MAX, 0)
    # Draw the result text
    screen.blit(result_surf, result_rect)

    pygame.display.flip()

    # Pause briefly to show the result
    pygame.time.wait(RESULT_PAUSE_DURATION_MS)

    # Optional: Wait for player input before returning
    # waiting_for_input = True
    # while waiting_for_input:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             exit()
    #         if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
    #             waiting_for_input = False
    #     clock.tick(30) # Keep event loop responsive


# --- Example Usage (Modified Main Loop) ---
if __name__ == '__main__':
    pygame.init()

    # --- Font Loading ---
    game_font = None
    try:
        # ... (font loading code remains the same) ...
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
    pygame.display.set_caption("Pythagoras Game - Missile Test")
    clock = pygame.time.Clock() # Create clock object

    # --- Game State ---
    # Define initial points (could be randomized in a real game)
    start_pos = (SCREEN_WIDTH // 5, SCREEN_HEIGHT * 4 // 5)
    target_pos = (SCREEN_WIDTH * 4 // 5, SCREEN_HEIGHT // 5)

    # Simulate getting player's guess (replace with actual input later)
    # Example: Calculate true length and make a guess slightly off
    dx = target_pos[0] - start_pos[0]
    dy = target_pos[1] - start_pos[1]
    true_hypot = math.hypot(dx, dy)
    # Simulate a guess that's, say, 80% of true length
    simulated_guess_px = true_hypot * 0.8
    players_guess_units = round(simulated_guess_px / 100.0) # Convert to units of 100px

    print(f"True hypotenuse: {true_hypot:.1f} px")
    print(f"Player's guess: {players_guess_units} (Simulating {players_guess_units*100} px)")

    # --- Main Loop Control ---
    state = "SHOW_TRIANGLE" # Initial state
    running = True

    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Add event handling for player input to guess here later
            if event.type == pygame.KEYDOWN:
                 if state == "SHOW_TRIANGLE" and event.key == pygame.K_SPACE:
                     # Trigger animation on space bar press (for testing)
                     state = "ANIMATING"
                 elif state == "POST_ANIMATION" and event.key == pygame.K_r:
                     # Reset for another round (example)
                     # Regenerate points, get new guess etc.
                     # For now, just go back to showing triangle
                     print("Resetting...")
                     # Example: randomize target slightly
                     target_pos = (target_pos[0] + 50) % SCREEN_WIDTH, (target_pos[1] - 50) % SCREEN_HEIGHT
                     dx = target_pos[0] - start_pos[0]
                     dy = target_pos[1] - start_pos[1]
                     true_hypot = math.hypot(dx, dy)
                     simulated_guess_px = true_hypot * (0.6 + 0.8 * (time.time() % 1.0)) # Vary guess %
                     players_guess_units = round(simulated_guess_px / 100.0)
                     print(f"New True hypotenuse: {int(true_hypot)} px")
                     print(f"New Player's guess: {players_guess_units} (Simulating {players_guess_units*100} px)")
                     state = "SHOW_TRIANGLE"


        # --- Game Logic & Drawing based on State ---
        if state == "SHOW_TRIANGLE":
            screen.fill(pygame.Color('black'))
            # Draw the initial triangle with labels
            draw_right_triangle_with_labels(screen, game_font,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            start_pos[0], start_pos[1],
                                            target_pos[0], target_pos[1])
            # Draw start/target points
            pygame.draw.circle(screen, pygame.Color('pink'), start_pos, 10)
            pygame.draw.circle(screen, pygame.Color('pink'), target_pos, 10)

            # Add text prompting player to guess or press space
            prompt_surf = game_font.render("Press SPACE to fire missile!", True, TEXT_COLOR)
            prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, FONT_SIZE))
            screen.blit(prompt_surf, prompt_rect)

            pygame.display.flip()
            clock.tick(30) # Lower FPS when just showing static scene

        elif state == "ANIMATING":
            # Call the animation function - it handles its own drawing loop
            animate_missile_and_explosion(
                screen, clock, game_font,
                SCREEN_WIDTH, SCREEN_HEIGHT,
                start_pos, target_pos,
                players_guess_units
            )
            # After animation finishes, move to a post-animation state
            state = "POST_ANIMATION"

        elif state == "POST_ANIMATION":
            # Screen already shows the final frame from the animation
            # Add text prompting player to Reset
            prompt_surf = game_font.render("Animation Complete. Press R to Reset.", True, TEXT_COLOR)
            prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, FONT_SIZE))
            # Need to redraw screen here if we want the prompt overlayed
            # Or the animation function could draw this on its last frame before pause
            # Let's redraw briefly:
            # Re-draw the last frame elements (or simplify)
            final_missile_end_vec = pygame.math.Vector2(start_pos) + (pygame.math.Vector2(target_pos)-pygame.math.Vector2(start_pos)).normalize() * (players_guess_units*100.0)
            explosion_center = (int(final_missile_end_vec.x), int(final_missile_end_vec.y))
            true_hypot = (pygame.math.Vector2(target_pos)-pygame.math.Vector2(start_pos)).length()

            screen.fill(pygame.Color('black'))
            if abs(target_pos[0] - start_pos[0]) > 0: pygame.draw.line(screen, TRIANGLE_COLOR, start_pos, (target_pos[0], start_pos[1]), LINE_WIDTH)
            if abs(target_pos[1] - start_pos[1]) > 0: pygame.draw.line(screen, TRIANGLE_COLOR, (target_pos[0], start_pos[1]), target_pos, LINE_WIDTH)
            if true_hypot > 0.01: pygame.draw.line(screen, HYPOTENUSE_COLOR, start_pos, target_pos, HYPOTENUSE_LINE_WIDTH)
            pygame.draw.circle(screen, pygame.Color('pink'), start_pos, 10)
            pygame.draw.circle(screen, pygame.Color('pink'), target_pos, 10)
            if players_guess_units*100.0 > 0.1: pygame.draw.line(screen, MISSILE_COLOR, start_pos, explosion_center, MISSILE_WIDTH)
            pygame.draw.circle(screen, EXPLOSION_COLOR_OUTER, explosion_center, EXPLOSION_RADIUS_OUTER_MAX, 0)
            pygame.draw.circle(screen, EXPLOSION_COLOR_INNER, explosion_center, EXPLOSION_RADIUS_INNER_MAX, 0)
            result_text = f"True Distance: {true_hypot:.1f}px"
            result_surf = game_font.render(result_text, True, RESULT_TEXT_COLOR)
            result_rect = result_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - FONT_SIZE * 2))
            screen.blit(result_surf, result_rect)
            # Now add the prompt
            screen.blit(prompt_surf, prompt_rect)

            pygame.display.flip()
            clock.tick(30)


    pygame.quit()