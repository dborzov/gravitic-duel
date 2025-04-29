import pygame

# --- Constants for Health Bar Style ---
# Colors (RGB)
COLOR_HEALTH_P1 = (0, 255, 0)      # Green for Player 1 health
COLOR_HEALTH_P2 = (255, 255, 0)    # Yellow for Player 2 health (or same as P1)
COLOR_DEPLETED = (100, 0, 0)     # Dark red for depleted health background
COLOR_BORDER = (200, 200, 200)   # Light gray for the border
COLOR_BACKGROUND = (50, 50, 50)  # Optional: Color for the area behind the bars

# Dimensions and Positioning
BAR_HEIGHT = 25
TOP_MARGIN = 20
SIDE_MARGIN = 20
BORDER_THICKNESS = 3
BAR_WIDTH_PERCENT = 0.4 # Percentage of screen width for each bar

# --- The Drawing Function ---

def draw_fighter_health_bars(screen, health1, max_health1, health2, max_health2):
    """
    Draws two fighting-game style health bars at the top of the screen.

    Args:
        screen (pygame.Surface): The main display surface to draw on.
        health1 (float or int): Current health of Player 1 (left side).
        max_health1 (float or int): Maximum possible health of Player 1.
        health2 (float or int): Current health of Player 2 (right side).
        max_health2 (float or int): Maximum possible health of Player 2.
    """
    screen_width = screen.get_width()
    bar_max_width = int(screen_width * BAR_WIDTH_PERCENT)

    # --- Input Validation / Clamping ---
    # Ensure health doesn't go below 0 for calculation purposes
    current_health1 = max(0, health1)
    current_health2 = max(0, health2)
    # Prevent division by zero if max_health is somehow zero
    if max_health1 <= 0: max_health1 = 1
    if max_health2 <= 0: max_health2 = 1

    # --- Calculate Health Ratios ---
    health_ratio1 = current_health1 / max_health1
    health_ratio2 = current_health2 / max_health2

    # --- Calculate Bar Widths ---
    current_bar_width1 = int(bar_max_width * health_ratio1)
    current_bar_width2 = int(bar_max_width * health_ratio2)

    # --- Define Bar Rectangles ---
    # Player 1 (Left)
    bg_rect1 = pygame.Rect(SIDE_MARGIN, TOP_MARGIN, bar_max_width, BAR_HEIGHT)
    health_rect1 = pygame.Rect(SIDE_MARGIN, TOP_MARGIN, current_bar_width1, BAR_HEIGHT)
    border_rect1 = pygame.Rect(
        SIDE_MARGIN - BORDER_THICKNESS,
        TOP_MARGIN - BORDER_THICKNESS,
        bar_max_width + (BORDER_THICKNESS * 2),
        BAR_HEIGHT + (BORDER_THICKNESS * 2)
    )

    # Player 2 (Right) - Note the x-coordinate calculation for health_rect2
    # The background starts from the right edge minus its width
    bg_rect2_x = screen_width - SIDE_MARGIN - bar_max_width
    bg_rect2 = pygame.Rect(bg_rect2_x, TOP_MARGIN, bar_max_width, BAR_HEIGHT)
    # The health bar's left edge moves left as health decreases.
    # Its right edge stays aligned with the background's right edge.
    health_rect2_x = screen_width - SIDE_MARGIN - current_bar_width2
    health_rect2 = pygame.Rect(health_rect2_x, TOP_MARGIN, current_bar_width2, BAR_HEIGHT)
    border_rect2 = pygame.Rect(
        bg_rect2_x - BORDER_THICKNESS,
        TOP_MARGIN - BORDER_THICKNESS,
        bar_max_width + (BORDER_THICKNESS * 2),
        BAR_HEIGHT + (BORDER_THICKNESS * 2)
    )

    # --- Draw the Bars ---
    # Optional: Draw a background panel behind the bars if desired
    # panel_height = BAR_HEIGHT + BORDER_THICKNESS * 2 + 10 # Example padding
    # panel_rect = pygame.Rect(0, TOP_MARGIN - BORDER_THICKNESS - 5, screen_width, panel_height)
    # pygame.draw.rect(screen, COLOR_BACKGROUND, panel_rect)

    # Player 1
    pygame.draw.rect(screen, COLOR_BORDER, border_rect1)      # Border first
    pygame.draw.rect(screen, COLOR_DEPLETED, bg_rect1)       # Then background (depleted)
    pygame.draw.rect(screen, COLOR_HEALTH_P1, health_rect1)  # Then current health

    # Player 2
    pygame.draw.rect(screen, COLOR_BORDER, border_rect2)      # Border first
    pygame.draw.rect(screen, COLOR_DEPLETED, bg_rect2)       # Then background (depleted)
    pygame.draw.rect(screen, COLOR_HEALTH_P2, health_rect2)  # Then current health


# --- Example Usage (within your Pygame main loop) ---

if __name__ == '__main__': # Example simulation if run directly
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Health Bar Demo")
    clock = pygame.time.Clock()

    # Dummy World and Rocket objects for demonstration
    class MockRocket:
        def __init__(self, max_hp):
            self.max_health = max_hp
            self.health = max_hp

    class MockWorld:
        def __init__(self):
            self.rocket1 = MockRocket(150)
            self.rocket2 = MockRocket(100) # Can have different max health

    world = MockWorld()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                 # Simulate damage
                if event.key == pygame.K_q: # Q damages P1
                    world.rocket1.health -= 10
                if event.key == pygame.K_p: # P damages P2
                    world.rocket2.health -= 10
                if event.key == pygame.K_r: # R resets health
                    world.rocket1.health = world.rocket1.max_health
                    world.rocket2.health = world.rocket2.max_health


        # --- Game Logic Update ---
        # (Your game logic here)
        # Clamp health in game logic if needed (optional here as draw func handles < 0)
        world.rocket1.health = max(0, world.rocket1.health)
        world.rocket2.health = max(0, world.rocket2.health)

        # --- Drawing ---
        screen.fill((30, 30, 30)) # Fill background (dark grey)

        # Call the health bar function using the world state
        draw_fighter_health_bars(
            screen,
            world.rocket1.health,
            world.rocket1.max_health,
            world.rocket2.health,
            world.rocket2.max_health
        )

        # (Draw other game elements like rockets, projectiles, etc.)

        # --- Update Display ---
        pygame.display.flip()

        # --- Frame Rate Control ---
        clock.tick(60) # Limit to 60 FPS

    pygame.quit()