import pygame
import sys
import argparse
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
import ui

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Gravitic Duel Game')
    parser.add_argument('--dev-mode', type=int, default=0,
                      help='Development mode (1-11)')
    return parser.parse_args()

def init_pygame():
    """Initialize Pygame and create the game window."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Gravitic Duel")
    clock = pygame.time.Clock()
    return screen, clock

def main():
    # Parse command line arguments
    args = parse_arguments()
    dev_mode = args.dev_mode

    # Initialize Pygame
    screen, clock = init_pygame()
    font = ui.init_font()

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Clear screen
        screen.fill(BLACK)

        # Dev mode 1: Display test message
        if dev_mode == 1:
            ui.draw_text(screen, "DEV MODE 1 ACTIVE", font)

        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)

    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 