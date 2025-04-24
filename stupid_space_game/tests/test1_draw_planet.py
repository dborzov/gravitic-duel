from .. import graphics
import pygame
import sys  

def test_draw_planet():
    screen = graphics.init_graphics()
    
    celestial_ids = [
        "planet0-star",
        "planet1-rock",
        "planet2-gas-giant",
        "planet3-lava",
        "planet4-earth",
        "planet5-ice",
        "planet6-mars",
        "planet7-water"
    ]
    celesital_graphics = [graphics.CelestialBodyGraphics(cid) for cid in celestial_ids]
    
    # Create font for captions
    font = pygame.font.Font(None, 36)
    
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        for num, (celestial, cid) in enumerate(zip(celesital_graphics, celestial_ids)):
            pos_x = (num+2)*250
            pos_y = 200
            celestial.draw(screen, pygame.math.Vector2(pos_x, pos_y))
            
            # Render and draw caption
            text = font.render(cid, True, (255, 255, 255))
            text_rect = text.get_rect(center=(pos_x, pos_y + 170))
            screen.blit(text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        clock.tick(30)

if __name__ == "__main__":
    test_draw_planet()
