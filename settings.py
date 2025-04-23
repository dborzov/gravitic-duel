import pygame

# Screen settings
SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1440
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font settings
FONT_SIZE = 48
FONT_NAME = None  # Will use Pygame's default font

# Asset directories
IMG_DIR = "assets"

# Key mappings
PLAYER1_UP = pygame.K_w
PLAYER1_DOWN = pygame.K_s
PLAYER1_LEFT = pygame.K_a
PLAYER1_RIGHT = pygame.K_d
PLAYER1_FIRE = pygame.K_q

PLAYER2_UP = pygame.K_KP8
PLAYER2_DOWN = pygame.K_KP2
PLAYER2_LEFT = pygame.K_KP4
PLAYER2_RIGHT = pygame.K_KP6
PLAYER2_FIRE = pygame.K_KP7
