import pygame
import math

# --- Constants (Adjust as needed) ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1440
TRIANGLE_COLOR = pygame.Color('yellow')     # Color for the triangle legs
TEXT_COLOR = pygame.Color('white')        # Color for the length labels
HYPOTENUSE_COLOR = pygame.Color('magenta')  # Bright purple/magenta for hypotenuse
LINE_WIDTH = 2                            # Thickness of the triangle legs
HYPOTENUSE_LINE_WIDTH = 4                 # Thickness for the hypotenuse
FONT_SIZE = 24                            # Font size for labels
TEXT_PADDING = 10                         # Pixels to offset text from lines

# --- Font Object Placeholder ---
# Defined later, after pygame.init()


def draw_right_triangle_with_labels(
    screen: pygame.Surface,
    font: pygame.font.Font,
    x_start: int,
    y_start: int,
    x_target: int,
    y_target: int
) -> None:
    """
    Draws a right-angled triangle on the Pygame screen connecting
    start and target points with legs parallel to the X and Y axes,
    and the hypotenuse connecting start and target directly.
    Also displays the lengths of the legs.

    Args:
        screen: The pygame.Surface object to draw onto.
        font: The pygame.font.Font object to use for rendering text.
        x_start: The x-coordinate of the starting point.
        y_start: The y-coordinate of the starting point.
        x_target: The x-coordinate of the target point.
        y_target: The y-coordinate of the target point.
    """
    # --- 1. Calculate Geometry ---
    corner_x = x_target
    corner_y = y_start
    delta_x = abs(x_target - x_start)
    delta_y = abs(y_target - y_start)

    # --- 2. Draw the Triangle Components ---
    # Horizontal leg: from start to corner
    pygame.draw.line(screen, TRIANGLE_COLOR,
                     (x_start, y_start), (corner_x, corner_y), LINE_WIDTH)

    # Vertical leg: from corner to target
    pygame.draw.line(screen, TRIANGLE_COLOR,
                     (corner_x, corner_y), (x_target, y_target), LINE_WIDTH)

    # Hypotenuse: from start to target  <--- ADDED
    pygame.draw.line(screen, HYPOTENUSE_COLOR,
                     (x_start, y_start), (x_target, y_target), HYPOTENUSE_LINE_WIDTH)


    # --- 3. Prepare and Render Text Labels (Using the passed font) ---
    text_horiz_str = f"{delta_x}px"
    text_horiz_surf = font.render(text_horiz_str, True, TEXT_COLOR)
    text_horiz_rect = text_horiz_surf.get_rect()

    text_vert_str = f"{delta_y}px"
    text_vert_surf = font.render(text_vert_str, True, TEXT_COLOR)
    text_vert_rect = text_vert_surf.get_rect()

    # --- 4. Position and Blit Text Labels ---
    # (Positioning logic remains the same)
    text_horiz_rect.centerx = (x_start + corner_x) // 2
    text_horiz_rect.top = corner_y + TEXT_PADDING

    text_vert_rect.centery = (corner_y + y_target) // 2
    text_vert_rect.left = corner_x + TEXT_PADDING

    corner_point = pygame.Vector2(corner_x, corner_y)
    # Basic check to nudge text away from corner if too close
    if pygame.Rect(text_horiz_rect).collidepoint(corner_point):
         text_horiz_rect.left += TEXT_PADDING if x_target > x_start else -TEXT_PADDING
    if pygame.Rect(text_vert_rect).collidepoint(corner_point):
         text_vert_rect.top += TEXT_PADDING if y_target > y_start else -TEXT_PADDING

    screen.blit(text_horiz_surf, text_horiz_rect)
    screen.blit(text_vert_surf, text_vert_rect)

# --- Example Usage (Standalone Test) ---
if __name__ == '__main__':
    pygame.init() # Initialize ALL Pygame modules FIRST

    # --- Create Font Object AFTER pygame.init() ---
    game_font = None
    try:
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
    pygame.display.set_caption("Pygame Right Triangle Drawer")

    start_pos = (300, 800)
    target_pos = (600, 400) # Initial target

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                 # On click, set the target to the mouse position
                 target_pos = event.pos
                 print(f"New Target: {target_pos}")


        # --- Drawing ---
        screen.fill(pygame.Color('black')) # Clear screen each frame

        # Draw the triangle (legs + hypotenuse) and labels using the function
        draw_right_triangle_with_labels(screen, game_font,
                                        start_pos[0], start_pos[1],
                                        target_pos[0], target_pos[1])

        # Optionally draw the start/target points for reference
        pygame.draw.circle(screen, pygame.Color('pink'), start_pos, 10)
        pygame.draw.circle(screen, pygame.Color('pink'), target_pos, 10)


        # --- Update Display ---
        pygame.display.flip() # Or pygame.display.update()

        clock.tick(60) # Limit frame rate

    pygame.quit()