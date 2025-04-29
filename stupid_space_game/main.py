import sys
import pygame
from stupid_space_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
import stupid_space_game.graphics as graphics
from stupid_space_game.world import World
from stupid_space_game.controls import player1_input_control,  player2_input_control, player_shoot_check
import stupid_space_game.ui as ui
import stupid_space_game.missile_logic as missile_logic


def main():
    screen = graphics.init_graphics()
    ui.ui_init()

    world = World()
    background = graphics.BackgroundGraphics()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        player1_input_control(keys, world.rocket1)
        player2_input_control(keys, world.rocket2)
        world.update()
        background.draw(screen)
        world.draw(screen)
        pygame.display.update()
        if player_shoot_check(keys, world):
            missile_logic.missile_minigame(screen, clock, world.rocket1.position, world.rocket2.position)
        clock.tick(30)

if __name__ == "__main__":
    main()
