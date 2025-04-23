import pygame
from settings import FONT_SIZE, FONT_NAME, WHITE

def init_font():
    """Initialize and return the game font."""
    return pygame.font.Font(FONT_NAME, FONT_SIZE)

def draw_text(screen, text, font, position=None, color=WHITE):
    """
    Draw text on the screen.
    
    Args:
        screen (pygame.Surface): The screen to draw on
        text (str): The text to draw
        font (pygame.font.Font): The font to use
        position (tuple, optional): The position to draw at. If None, centers the text.
        color (tuple, optional): The color to draw in. Defaults to white.
    """
    text_surface = font.render(text, True, color)
    if position is None:
        # Center the text
        position = (
            (screen.get_width() - text_surface.get_width()) // 2,
            (screen.get_height() - text_surface.get_height()) // 2
        )
    screen.blit(text_surface, position) 