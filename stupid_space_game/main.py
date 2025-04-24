import sys
import pygame
from stupid_space_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
import stupid_space_game.graphics as graphics

def main():
    screen = graphics.init_graphics()


    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
