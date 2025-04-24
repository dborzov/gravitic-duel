from .. import graphics
import pygame
import sys  
import math

def test_draw_rocket():
    screen = graphics.init_graphics()
    rocket = graphics.RocketGraphics()
    
    clock = pygame.time.Clock()
    angles = [n*360 / 8 for n in range(0, 10)]
    font = pygame.font.Font(None, 36)

    while True:
        for id,angle in enumerate(angles):
            rocket.draw(screen, (500 + id*200, 500), angle)
            text = font.render(f"{angle:.2f}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(500 + id*200, 400))
            screen.blit(text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        clock.tick(30)

if __name__ == "__main__":
    test_draw_rocket()