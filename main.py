import pygame
from game import Game
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, BLOCK_SIZE


def main():
    pygame.init()

    # Screen dimensions for two boards
    screen = pygame.display.set_mode((SCREEN_WIDTH * 2, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris Battle")
    clock = pygame.time.Clock()

    # Create two Game instances
    # player1_game = Game()
    player2_game = Game()

    # fall_time_p1 = 0
    fall_time_p2 = 0

    running = True
    while running:
        screen.fill(COLORS["0"])  # Clear the screen
        delta_time = clock.tick(30)

        # Update fall times
        # fall_time_p1 += delta_time
        fall_time_p2 += delta_time

        # if fall_time_p1 > 500:  # Player 1 drop interval
        #     player1_game.drop(screen)
        #     fall_time_p1 = 0

        if fall_time_p2 > 500:  # Player 2 drop interval
            player2_game.drop(screen)
            fall_time_p2 = 0

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Player 1 controls
                # if event.key == pygame.K_w:
                #     player1_game.rotateMino()
                # elif event.key == pygame.K_a:
                #     player1_game.move(-1, 0)
                # elif event.key == pygame.K_d:
                #     player1_game.move(1, 0)
                # elif event.key == pygame.K_s:
                #     player1_game.drop(screen)

                # Player 2 controls
                if event.key == pygame.K_UP:
                    player2_game.rotateMino()
                elif event.key == pygame.K_LEFT:
                    player2_game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player2_game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    player2_game.drop(screen)

        # Check for game over
        # if player1_game.game_over or player2_game.game_over:
        #     running = False
        if player2_game.game_over:
            running = False

        # Draw both game boards
        # player1_game.drawGrid(screen, offset_x=0)  # Player 1 on the left
        # player1_game.drawMino(screen, offset_x=0)
        # player1_game.renderScore(screen, offset_x=10, offset_y=10)

        # Player 2 on the right
        player2_game.drawGrid(screen, offset_x=SCREEN_WIDTH)
        player2_game.drawMino(screen, offset_x=SCREEN_WIDTH)
        player2_game.renderScore(
            screen, offset_x=SCREEN_WIDTH - 290, offset_y=20)
        player2_game.renderLevel(
            screen, offset_x=SCREEN_WIDTH - 290, offset_y=50)
        player2_game.renderWhitePoints(
            screen, offset_x=SCREEN_WIDTH - 290, offset_y=80)
        player2_game.renderRedRule(
            screen, offset_x=SCREEN_WIDTH - 290, offset_y=110)

        # separator_width = 5
        # pygame.draw.rect(
        #     screen,
        #     (255, 255, 255),  
        #     (
        #         SCREEN_WIDTH - separator_width // 2,  
        #         0,                                  
        #         separator_width,                   
        #         SCREEN_HEIGHT                      
        #     )
        # )

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

