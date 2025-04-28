import pygame
import math

# --- Constants (Adjust as needed) ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1440
TRIANGLE_COLOR = pygame.Color('yellow')
TEXT_COLOR = pygame.Color('white')
HYPOTENUSE_COLOR = pygame.Color('magenta')
LINE_WIDTH = 2
HYPOTENUSE_LINE_WIDTH = 4
FONT_SIZE = 24
TEXT_PADDING = 10 # Min distance between text and its corresponding line
MIN_LABEL_LENGTH = 1 # Don't draw labels for lines shorter than this


def clamp_rect_to_screen(rect: pygame.Rect, screen_width: int, screen_height: int) -> pygame.Rect:
    """Adjusts a Rect to attempt to stay fully within screen boundaries."""
    # Create a copy to avoid modifying the original if it's reused elsewhere
    clamped_rect = rect.copy()

    # Use clamp method for cleaner boundary checks
    clamped_rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))

    # Note: clamp_ip might change width/height if the original rect was
    # larger than the screen. For just position clamping:
    # Original rect position relative to screen edges
    # if clamped_rect.left < 0: clamped_rect.left = 0
    # if clamped_rect.right > screen_width: clamped_rect.right = screen_width
    # if clamped_rect.top < 0: clamped_rect.top = 0
    # if clamped_rect.bottom > screen_height: clamped_rect.bottom = screen_height

    return clamped_rect

def draw_hypotenuse_guess(    screen: pygame.Surface,
    font: pygame.font.Font,
    screen_width: int, # Pass screen dimensions for clamping
    screen_height: int,
    x_start: int,
    y_start: int,
    x_target: int,
    y_target: int
) -> None:
    
    
def draw_right_triangle_with_labels(
    screen: pygame.Surface,
    font: pygame.font.Font,
    screen_width: int, # Pass screen dimensions for clamping
    screen_height: int,
    x_start: int,
    y_start: int,
    x_target: int,
    y_target: int
) -> None:
    """
    Draws a right-angled triangle and labels with robust positioning.

    Handles different relative start/target positions and ensures labels
    are placed outside the triangle and clamped to screen boundaries.
    Doesn't draw labels for zero-length sides.

    Args:
        screen: The pygame.Surface object to draw onto.
        font: The pygame.font.Font object for rendering text.
        screen_width: Width of the screen for boundary clamping.
        screen_height: Height of the screen for boundary clamping.
        x_start, y_start: Coordinates of the starting point.
        x_target, y_target: Coordinates of the target point.
    """
    # --- 1. Calculate Geometry ---
    corner_x = x_target
    corner_y = y_start
    delta_x = abs(x_target - x_start)
    delta_y = abs(y_target - y_start)

    # --- 2. Draw the Triangle Components ---
    # Only draw lines if they have some length to avoid drawing points
    # Horizontal leg (y = y_start)
    if delta_x > 0:
        pygame.draw.line(screen, TRIANGLE_COLOR,
                         (x_start, y_start), (corner_x, corner_y), LINE_WIDTH)
    # Vertical leg (x = x_target)
    if delta_y > 0:
        pygame.draw.line(screen, TRIANGLE_COLOR,
                         (corner_x, corner_y), (x_target, y_target), LINE_WIDTH)

    # Hypotenuse (always draw if start != target)
    if delta_x > 0 or delta_y > 0:
        pygame.draw.line(screen, HYPOTENUSE_COLOR,
                         (x_start, y_start), (x_target, y_target), HYPOTENUSE_LINE_WIDTH)

    # --- 3. Render, Position, Clamp, and Blit Labels ---

    # --- Horizontal Label (Describes Delta X) ---
    if delta_x >= MIN_LABEL_LENGTH:
        text_horiz_str = f"{delta_x}px"
        text_horiz_surf = font.render(text_horiz_str, True, TEXT_COLOR)
        text_horiz_rect = text_horiz_surf.get_rect()

        # Center horizontally along the line segment
        text_horiz_rect.centerx = (x_start + x_target) // 2

        # Position vertically "outside" the triangle, relative to the horizontal line (y=y_start)
        if y_target <= y_start:  # Target is above or level with start: Place text BELOW line
            text_horiz_rect.top = y_start + TEXT_PADDING
        else:  # Target is below start: Place text ABOVE line
            text_horiz_rect.bottom = y_start - TEXT_PADDING

        # Clamp the final position to screen boundaries
        final_horiz_rect = clamp_rect_to_screen(text_horiz_rect, screen_width, screen_height)
        screen.blit(text_horiz_surf, final_horiz_rect)

    # --- Vertical Label (Describes Delta Y) ---
    if delta_y >= MIN_LABEL_LENGTH:
        text_vert_str = f"{delta_y}px"
        text_vert_surf = font.render(text_vert_str, True, TEXT_COLOR)
        text_vert_rect = text_vert_surf.get_rect()

        # Center vertically along the line segment
        text_vert_rect.centery = (y_start + y_target) // 2

        # Position horizontally "outside" the triangle, relative to the vertical line (x=x_target)
        if x_target >= x_start:  # Target is right or level with start: Place text RIGHT of line
            text_vert_rect.left = x_target + TEXT_PADDING
        else:  # Target is left of start: Place text LEFT of line
            text_vert_rect.right = x_target - TEXT_PADDING

        # Clamp the final position to screen boundaries
        final_vert_rect = clamp_rect_to_screen(text_vert_rect, screen_width, screen_height)
        screen.blit(text_vert_surf, final_vert_rect)


# --- Example Usage (Standalone Test) ---
if __name__ == '__main__':
    pygame.init()

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
    pygame.display.set_caption("Pygame Right Triangle Drawer - Robust")

    # Test various start/target positions by clicking
    start_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT * 3 // 4) # Start bottom-left quadrant
    target_pos = (SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 4) # Initial target top-right quadrant

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                 if event.button == 1: # Left click sets target
                     target_pos = event.pos
                     print(f"New Target: {target_pos}")
                 elif event.button == 3: # Right click sets start
                     start_pos = event.pos
                     print(f"New Start: {start_pos}")


        screen.fill(pygame.Color('black'))

        # Call the drawing function, passing screen dimensions
        draw_right_triangle_with_labels(screen, game_font,
                                        SCREEN_WIDTH, SCREEN_HEIGHT, # Pass dimensions
                                        start_pos[0], start_pos[1],
                                        target_pos[0], target_pos[1])

        # Draw points for clarity
        pygame.draw.circle(screen, pygame.Color('pink'), start_pos, 10)
        pygame.draw.circle(screen, pygame.Color('pink'), target_pos, 10)
        # Draw corner point for debugging/visualization
        corner_x = target_pos[0]
        corner_y = start_pos[1]
        pygame.draw.circle(screen, pygame.Color('cyan'), (corner_x, corner_y), 3)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()