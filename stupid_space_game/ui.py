import pygame

GAME_FONT: pygame.font.Font = None
LARGE_FONT: pygame.font.Font = None

numbers_ui = None
FONT_SIZE = 34


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