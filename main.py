import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    fallTime = 0

    running = True
    while running:
        screen.fill((0, 0, 0))
        fallTime += clock.get_rawtime()
        clock.tick(30)

        if fallTime > 50:
            fallTime = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

