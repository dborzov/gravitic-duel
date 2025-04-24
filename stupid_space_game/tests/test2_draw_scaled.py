from .. import graphics
import pygame
import sys  

def test_draw_planet():
    screen = graphics.init_graphics()
    radii = [50, 100, 150, 200, 250, 300]
    celesitals = [graphics.CelestialBodyGraphics("planet4-earth", radius) for radius in radii]
    
    # Create font for captions
    font = pygame.font.Font(None, 36)
    
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        for num, (celestial, radius) in enumerate(zip(celesitals, radii)):
            pos_x = (num+2)*250
            pos_y = 1000
            celestial.draw(screen, (pos_x, pos_y))
            
            # Render and draw caption
            text = font.render(f"{radius}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(pos_x, pos_y - radius - 70))
            screen.blit(text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        clock.tick(30)

if __name__ == "__main__":
    test_draw_planet()
