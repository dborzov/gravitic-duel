import pygame
from pygame.math import Vector2
from stupid_space_game.ui import get_game_font, get_numbers_ui, get_large_font
from stupid_space_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, MISSILE_GRAIN

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
EXPLOSION_RADIUS_INNER_MAX = MISSILE_GRAIN // 2
EXPLOSION_RADIUS_OUTER_MAX = MISSILE_GRAIN
EXPLOSION_DURATION_MS = 300

# Define Text Colors Globally
TEXT_COLOR = pygame.Color('white') # Default for initial side labels
RESULT_TEXT_COLOR = pygame.Color('cyan') # For side labels in final state
GUESS_VS_TRUE_COLOR = pygame.Color('lime') # For the guess/true comparison label
PROMPT_TEXT_COLOR = pygame.Color('lightgray') # For user prompts

def clamp_rect_to_screen(rect: pygame.Rect) -> pygame.Rect:
    """Clamps a rectangle to the screen boundaries defined by global constants."""
    clamped_rect = rect.copy()
    # Use global constants directly
    clamped_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    return clamped_rect

def animate_missile_and_explosion(
    screen: pygame.Surface,
    original_frame: pygame.Surface,
    clock: pygame.time.Clock, # Use the imported Clock
    start_vec: Vector2,    # Use Vector2
    target_vec: Vector2,   # Use Vector2
    players_guess: int
):
    """Animates missile flight and explosion using Vector2."""
    guessed_length_px = players_guess * MISSILE_GRAIN
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
        dt = clock.tick(160)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()

        elapsed_time_frame = dt
        current_missile_length += MISSILE_SPEED_PPT * (elapsed_time_frame / 1000.0)
        current_missile_length = min(current_missile_length, guessed_length_px)

        missile_end_vec = start_vec + unit_vec * current_missile_length
        missile_end_pos_tuple = (int(missile_end_vec.x), int(missile_end_vec.y)) # Tuple for drawing

        # Redraw basic scene for animation frame
        screen.blit(original_frame, (0, 0))
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
        dt = clock.tick(160)
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
    start_vec: Vector2,       # Use Vector2
    target_vec: Vector2,      # Use Vector2
    players_guess: int
) -> int:
    """Draws final scene using Vector2, global font, colors, and screen dimensions."""
    # GAME_FONT check removed, using get_game_font() directly

    # --- Calculations ---
    result_damage = 0
    guessed_length_px = players_guess * MISSILE_GRAIN
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
        text_horiz_str = f"{int(delta_x) // MISSILE_GRAIN}"
        # Use get_game_font()
        text_horiz_surf = get_game_font().render(text_horiz_str, True, RESULT_TEXT_COLOR)
        text_horiz_rect = text_horiz_surf.get_rect(centerx=int((start_vec.x + target_vec.x) / 2))
        if target_vec.y <= start_vec.y: text_horiz_rect.top = int(start_vec.y + TEXT_PADDING)
        else: text_horiz_rect.bottom = int(start_vec.y - TEXT_PADDING)
        # Use clamp_rect_to_screen without screen dimensions
        final_horiz_rect = clamp_rect_to_screen(text_horiz_rect)
        screen.blit(text_horiz_surf, final_horiz_rect)
    if delta_y >= MIN_LABEL_LENGTH:
        text_vert_str = f"{int(delta_y) // MISSILE_GRAIN}"
        # Use get_game_font()
        text_vert_surf = get_game_font().render(text_vert_str, True, RESULT_TEXT_COLOR)
        text_vert_rect = text_vert_surf.get_rect(centery=int((start_vec.y + target_vec.y) / 2))
        if target_vec.x >= start_vec.x: text_vert_rect.left = int(target_vec.x + TEXT_PADDING)
        else: text_vert_rect.right = int(target_vec.x - TEXT_PADDING)
        # Use clamp_rect_to_screen without screen dimensions
        final_vert_rect = clamp_rect_to_screen(text_vert_rect)
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

    result = "Missed!"
    if abs(true_length - players_guess*MISSILE_GRAIN) <= EXPLOSION_RADIUS_INNER_MAX:
        result = f"Bullseye!"
        precision = 1 + 10*abs(players_guess - true_length / MISSILE_GRAIN)
        result_damage = 100 / precision
    elif abs(true_length - players_guess*MISSILE_GRAIN) <= EXPLOSION_RADIUS_OUTER_MAX:
        result = "Scratched!"
        result_damage = 20

    guess_vs_true_text = f"{result} | Missile: {players_guess} | true distance: {true_length / MISSILE_GRAIN: .1f}"
    prompt_surf = get_large_font().render(guess_vs_true_text, True, PROMPT_TEXT_COLOR)
    prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, 3*FONT_SIZE))
    screen.blit(prompt_surf, prompt_rect)
    return result_damage



def draw_right_triangle_with_labels(
    screen: pygame.Surface,
    start_vec: Vector2,
    target_vec: Vector2,
) -> None:
    """Draws the basic triangle with side labels using Vector2, global font and screen dimensions."""
    # game_font = get_game_font() # Removed local variable

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

    # --- 3. Render, Position, Clamp, and Blit Labels (using get_game_font(), TEXT_COLOR) ---
    if delta_x >= MIN_LABEL_LENGTH:
        text_horiz_str = f"{int(delta_x / MISSILE_GRAIN)}" # Use .0f for cleaner int display
        # Use get_game_font()
        text_horiz_surf = get_game_font().render(text_horiz_str, True, TEXT_COLOR)
        text_horiz_rect = text_horiz_surf.get_rect(centerx=int((start_vec.x + target_vec.x) / 2))
        # Position using vector components
        if target_vec.y <= start_vec.y: text_horiz_rect.top = int(start_vec.y + TEXT_PADDING)
        else: text_horiz_rect.bottom = int(start_vec.y - TEXT_PADDING)
        # Use clamp_rect_to_screen without screen dimensions
        final_horiz_rect = clamp_rect_to_screen(text_horiz_rect)
        screen.blit(text_horiz_surf, final_horiz_rect)

    if delta_y >= MIN_LABEL_LENGTH:
        text_vert_str = f"{int(delta_y / MISSILE_GRAIN)}"
        # Use get_game_font()
        text_vert_surf = get_game_font().render(text_vert_str, True, TEXT_COLOR)
        text_vert_rect = text_vert_surf.get_rect(centery=int((start_vec.y + target_vec.y) / 2))
        # Position using vector components
        if target_vec.x >= start_vec.x: text_vert_rect.left = int(target_vec.x + TEXT_PADDING)
        else: text_vert_rect.right = int(target_vec.x - TEXT_PADDING)
        # Use clamp_rect_to_screen without screen dimensions
        final_vert_rect = clamp_rect_to_screen(text_vert_rect)
        screen.blit(text_vert_surf, final_vert_rect)

def round_down(x: int, grain: int):
    return (x // grain) * grain

def missile_minigame(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    start_vec: Vector2,
    target_vec: Vector2,
):  
    diff_vector =  start_vec - target_vec
    diff_vector.x = round_down(diff_vector.x, MISSILE_GRAIN)
    diff_vector.y = round_down(diff_vector.y, MISSILE_GRAIN)
    start_vec = target_vec + diff_vector

    original_frame = screen.convert() 
    state = "SHOW_TRIANGLE"
    running = True
    # Initialize players_guess_units; it will be updated on click
    players_guess_units = None
    result_damage = 0
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit() # Ensure pygame quits properly
                exit() # Exit the script
            if event.type == pygame.KEYDOWN:
                 if state == "SHOW_TRIANGLE":
                     if event.key == pygame.K_1:
                        players_guess_units = 1
                     elif event.key == pygame.K_2:
                        players_guess_units = 2
                     elif event.key == pygame.K_3:
                        players_guess_units = 3
                     elif event.key == pygame.K_4:
                        players_guess_units = 4
                     elif event.key == pygame.K_5:
                        players_guess_units = 5
                     elif event.key == pygame.K_6:
                        players_guess_units = 6
                     elif event.key == pygame.K_7:
                        players_guess_units = 7
                     elif event.key == pygame.K_8:
                        players_guess_units = 8
                     elif event.key == pygame.K_9:
                        players_guess_units = 9
                     elif event.key == pygame.K_0:
                        players_guess_units = 10

                     if players_guess_units is not None:
                        print(f"Firing with guess: {players_guess_units} units") # Debug
                        state = "ANIMATING"
                 elif state == "POST_ANIMATION":
                    return result_damage


        # --- Game Logic & Drawing based on State ---
        if state == "SHOW_TRIANGLE":
            screen.blit(original_frame, (0, 0))
            # Draw initial triangle using vectors and global font/dimensions
            # Removed SCREEN_WIDTH, SCREEN_HEIGHT from call
            # Draw circles using vector components as tuples
            pygame.draw.circle(screen, pygame.Color('pink'), (int(start_vec.x), int(start_vec.y)), 10)
            pygame.draw.circle(screen, pygame.Color('pink'), (int(target_vec.x), int(target_vec.y)), 10)

            # Use get_game_font()
            prompt_surf = get_game_font().render("Choose how far to launch the missile", True, PROMPT_TEXT_COLOR)
            prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, 7*FONT_SIZE)) # Use global SCREEN_WIDTH
            numbers_ui = get_numbers_ui()
            numbers_rect = numbers_ui.get_rect()
            numbers_rect.centerx = SCREEN_WIDTH // 2
            numbers_rect.top = 50
            screen.blit(numbers_ui, numbers_rect)
            screen.blit(prompt_surf, prompt_rect)
            draw_right_triangle_with_labels(screen, start_vec, target_vec)

            pygame.display.flip()
            clock.tick(30) # Use the passed clock object

        elif state == "ANIMATING":
            animate_missile_and_explosion(
                screen, original_frame, clock,
                start_vec, target_vec,
                players_guess_units
            )
            state = "POST_ANIMATION"

        elif state == "POST_ANIMATION":
            screen.blit(original_frame, (0, 0))
            # Draw final state using vectors and global font/dimensions
            # Removed screen dimension arguments
            result_damage = draw_final_state(screen,
                             start_vec, target_vec,
                             players_guess_units)

            pygame.display.flip()
            clock.tick(30) # Use the passed clock object

    # Added explicit quit call if loop finishes unexpectedly (e.g., if running becomes False differently)
    # Although the QUIT event above should handle normal exit.
    # pygame.quit() # This might interfere if this minigame is part of a larger app
    # exit()
