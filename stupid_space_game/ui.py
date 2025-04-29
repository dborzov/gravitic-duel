import pygame

GAME_FONT: pygame.font.Font = None
LARGE_FONT: pygame.font.Font = None

numbers_ui = None
FONT_SIZE = 34

# --- Constants for Health Bar Style ---
# Colors (RGB)
COLOR_MANA_TEXT = (255, 255, 255)  # Light blue for mana text
TEXT_PADDING = 10                # Pixels between bar and text
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

def ui_init():
    global GAME_FONT, LARGE_FONT, numbers_ui
    print("Initializing UI")
    GAME_FONT = pygame.font.Font(None, 24)
    LARGE_FONT = pygame.font.Font(None, 48)
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
         raise ValueError("CRITICAL: Font initialization failed. Exiting.")
    
    numbers_ui = pygame.image.load('./assets/numbers.png').convert_alpha()

def get_game_font():
    return GAME_FONT

def get_large_font():
    return LARGE_FONT

def get_numbers_ui():
    return numbers_ui


def draw_fighter_ui(screen, 
                    health1, max_health1, mana1, 
                    health2, max_health2, mana2):
    screen_width = screen.get_width()
    bar_max_width = int(screen_width * BAR_WIDTH_PERCENT)

    # --- Input Validation / Clamping ---
    current_health1 = max(0, health1)
    current_mana1 = max(0, mana1)
    current_health2 = max(0, health2)
    current_mana2 = max(0, mana2)



    # --- Calculate Ratios ---
    health_ratio1 = current_health1 / max_health1
    health_ratio2 = current_health2 / max_health2

    # --- Calculate Bar Widths ---
    current_bar_width1 = int(bar_max_width * health_ratio1)
    current_bar_width2 = int(bar_max_width * health_ratio2)

    # --- Define Bar Rectangles (Same as before) ---
    # Player 1 (Left)
    bg_rect1 = pygame.Rect(SIDE_MARGIN, TOP_MARGIN, bar_max_width, BAR_HEIGHT)
    health_rect1 = pygame.Rect(SIDE_MARGIN, TOP_MARGIN, current_bar_width1, BAR_HEIGHT)
    border_rect1 = pygame.Rect(
        SIDE_MARGIN - BORDER_THICKNESS,
        TOP_MARGIN - BORDER_THICKNESS,
        bar_max_width + (BORDER_THICKNESS * 2),
        BAR_HEIGHT + (BORDER_THICKNESS * 2)
    )
    # Player 2 (Right)
    bg_rect2_x = screen_width - SIDE_MARGIN - bar_max_width
    bg_rect2 = pygame.Rect(bg_rect2_x, TOP_MARGIN, bar_max_width, BAR_HEIGHT)
    health_rect2_x = screen_width - SIDE_MARGIN - current_bar_width2
    health_rect2 = pygame.Rect(health_rect2_x, TOP_MARGIN, current_bar_width2, BAR_HEIGHT)
    border_rect2 = pygame.Rect(
        bg_rect2_x - BORDER_THICKNESS,
        TOP_MARGIN - BORDER_THICKNESS,
        bar_max_width + (BORDER_THICKNESS * 2),
        BAR_HEIGHT + (BORDER_THICKNESS * 2)
    )

    # --- Draw Health Bars (Same as before) ---
    pygame.draw.rect(screen, COLOR_BORDER, border_rect1)
    pygame.draw.rect(screen, COLOR_DEPLETED, bg_rect1)
    pygame.draw.rect(screen, COLOR_HEALTH_P1, health_rect1)

    pygame.draw.rect(screen, COLOR_BORDER, border_rect2)
    pygame.draw.rect(screen, COLOR_DEPLETED, bg_rect2)
    pygame.draw.rect(screen, COLOR_HEALTH_P2, health_rect2)

    # --- Mana Text ---

    # Format Text Strings
    mana_text_str1 = f"{int(mana1)}%"
    mana_text_str2 = f"{int(mana2)}%"

    # Render Text Surfaces (Anti-aliased)
    mana_surf1 = GAME_FONT.render(mana_text_str1, True, COLOR_MANA_TEXT)
    mana_surf2 = GAME_FONT.render(mana_text_str2, True, COLOR_MANA_TEXT)

    # Get Text Rects and Position Them
    mana_rect1 = mana_surf1.get_rect()
    mana_rect2 = mana_surf2.get_rect()

    # Position P1 text to the right of P1 health bar
    mana_rect1.midleft = (border_rect1.right + TEXT_PADDING, border_rect1.centery)

    # Position P2 text to the left of P2 health bar
    mana_rect2.midright = (border_rect2.left - TEXT_PADDING, border_rect2.centery)

    # Blit Mana Text
    screen.blit(mana_surf1, mana_rect1)
    screen.blit(mana_surf2, mana_rect2)
