import pygame
from settings import FONT_SIZE, FONT_NAME, WHITE

def init_font():
    """Initialize the game font."""
    return pygame.font.Font(FONT_NAME, FONT_SIZE)

def draw_text(screen, text, font, color=WHITE):
    """
    Draw text centered on the screen.
    
    Args:
        screen: Pygame surface to draw on
        text: Text string to display
        font: Pygame font object
        color: RGB color tuple (default: WHITE)
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    screen.blit(text_surface, text_rect) 