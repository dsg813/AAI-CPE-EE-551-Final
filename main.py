import pygame
from game import Game
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Game()
    fallTime = 0

    running = True
    while running:
        # Use the background color from the COLORS dictionary
        screen.fill(COLORS["0"])
        fallTime += clock.get_rawtime()
        clock.tick(30)

        if fallTime > 50:
            game.drop(screen)  # Pass the screen to drop
            fallTime = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_UP:
                    game.rotate_mino()

        # Handle continuous downward movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            game.drop(screen)  # Pass the screen to drop

        if game.game_over:
            running = False

        game.drawGrid(screen)
        game.drawMino(screen)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()