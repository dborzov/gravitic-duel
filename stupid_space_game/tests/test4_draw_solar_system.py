import sys
import pygame
from stupid_space_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
import stupid_space_game.graphics as graphics
from stupid_space_game.world import World

def test4_draw_solar_system():
    screen = graphics.init_graphics()
    world = World()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        world.update()
        world.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    test4_draw()

