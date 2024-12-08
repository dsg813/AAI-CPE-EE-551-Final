import pygame
from game import Game
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, set_boardStateList, get_boardStateList, getWhite, setWhite

CELL_SIZE = 20
MARGIN = 2

def redraw_game_state(screen, game, board_state):
    """Redraw the game state on the screen."""
    game.setBoard(board_state)  # Update the game state with the given board
    screen.fill(COLORS["0"])  # Clear the screen with the background color
    game.drawGrid(screen, offset_x=0)  # Draw the grid on the left

    # Calculate white points and cells earned
    white_points = getWhite()
    white_cells = white_points // 8

    # Construct the f-string for the text to display
    text_to_display = construct_text_to_display(game, white_points, white_cells)

    # Always render text to the right of the game board
    game.renderText(screen, text=text_to_display, offset_x=SCREEN_WIDTH + 20, initial_offset_y=20)

    pygame.display.flip()  # Update the display


def detect_c_to_s_change(board_a, board_b):
    """
    Detects if a cell changes from 'C' to 'S' between two boards.
    """
    for y in range(len(board_a)):
        for x in range(len(board_a[0])):
            if board_a[y][x][1] == "C" and board_b[y][x][1] == "S":
                return True
    return False


def all_changes_c_to_s(boardStateList):
    """
    Checks if all changes in the boardStateList are 'C' to 'S'.
    """
    for i in range(1, len(boardStateList)):
        if not detect_c_to_s_change(boardStateList[i - 1], boardStateList[i]):
            return False
    return True



def display_board_states(screen, game):
    """Displays the progression of board states in `boardStateList` with scoring."""
    # Updated Delay Configurations
    INITIAL_FRAME_DELAY = 750  # 0.75 second for the first frame
    FRAME_DELAY = 250  # 0.25 seconds between frames
    BLINK_DELAY = 350  # 0.35 seconds for blinking

    boardStateList = get_boardStateList()

    if not boardStateList:
        return

    # Calculate the number of erased cells
    erased_count = sum(
        1
        for row in boardStateList[-1]
        for cell in row
        if cell == "0000-00"
    ) - sum(
        1
        for row in boardStateList[0]
        for cell in row
        if cell == "0000-00"
    )

    # Initialize points earned
    points_earned = 0

    # Determine points earned based on erased cells
    if erased_count > 0:
        if erased_count <= 8:
            points_earned += erased_count  # 1 point per erased cell
        else:
            points_earned += (8 + (erased_count - 8) * 2)  # 2 points per extra cell

    # Update the white points using setWhite
    setWhite(getWhite() + points_earned)
    # print(f"Points Earned During Animation: {points_earned}")
    # print(f"New White Score: {getWhite()}")

    # Adjust delays for smaller boardStateLists
    if len(boardStateList) < 8:
        INITIAL_FRAME_DELAY //= 2
        FRAME_DELAY //= 2
        BLINK_DELAY //= 2

    # Speed up if all changes are C-to-S
    if all_changes_c_to_s(boardStateList):
        # print("All changes are C-to-S; running twice as fast")
        INITIAL_FRAME_DELAY //= 2
        FRAME_DELAY //= 2
        BLINK_DELAY //= 2

    # If there are 2 or fewer states, instantly redraw the final frame and exit
    if len(boardStateList) <= 2:
        # print("Redrawing Final Frame Instantly (Frame Count <= 2)")
        redraw_game_state(screen, game, boardStateList[-1])
        set_boardStateList([])  # Clear the list
        return

    # Find the latest frame index where a C-to-S change occurred
    latest_c_to_s_index = -1
    for i in range(1, len(boardStateList)):
        if detect_c_to_s_change(boardStateList[i - 1], boardStateList[i]):
            latest_c_to_s_index = i

    # Draw all frames up to the latest C-to-S change
    # print("Drawing all frames up to the latest C-to-S change")
    for i, board_state in enumerate(boardStateList[:latest_c_to_s_index + 1]):
        # print(f"Displaying Board State {i}")

        # Redraw and delay
        redraw_game_state(screen, game, board_state)
        pygame.time.delay(FRAME_DELAY)

    # Blink between frame 0, latest C-to-S change frame, and final frame
    if latest_c_to_s_index > 0:
        # print("Blinking between Initial, Latest C-to-S, and Final Frame")
        for _ in range(2):  # Blink twice
            # Show the initial frame
            redraw_game_state(screen, game, boardStateList[0])
            pygame.time.delay(BLINK_DELAY)

            # Show the latest C-to-S frame
            redraw_game_state(screen, game, boardStateList[latest_c_to_s_index])
            pygame.time.delay(BLINK_DELAY)

            # Show the final frame
            redraw_game_state(screen, game, boardStateList[-1])
            pygame.time.delay(BLINK_DELAY)

    # Ensure we end with the final frame
    # print("Ending on Final Frame")
    redraw_game_state(screen, game, boardStateList[-1])

    # Clear `boardStateList` after displaying all states
    set_boardStateList([])
    # print("Debug: boardStateList cleared")

    # Force a new tetrimino spawn to handle premature spawns
    game.forceSpawnNewMino()
    # print("Forced spawn of new tetrimino to reset premature spawn")




def construct_text_to_display(game, white_points, white_cells):
    """
    Constructs the f-string for dynamic text display.

    :param game: The current Game instance
    :param white_points: Updated white points after animation
    :param white_cells: White cells earned (integer division of white points by 8)
    :return: A formatted string for rendering
    """
    return (
        f"Score: {game.score}\n"
        f"Level: {len(COLORS)-2}\n"
        f"White Points: {white_points}\n"
        f"White Cells Earned: {white_cells}\n"
        f"8 points per cell\n"
        f"8 red burns nearby cells\n"
        f"8 white goes to next level\n"
    )


def main():
    pygame.init()

    # Screen dimensions for a single board
    screen = pygame.display.set_mode((SCREEN_WIDTH + 300, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Create a Game instance
    player_game = Game()

    # Time tracking for delays
    fall_time = 0
    move_cooldown = 0  # Cooldown timer for smoother movement

    # Flag to track if an animation is running
    is_animating = False

    running = True
    while running:
        screen.fill(COLORS["0"])  # Clear the screen
        delta_time = clock.tick(30)  # Maintain 30 FPS

        # Update fall time and cooldowns
        fall_time += delta_time
        move_cooldown += delta_time

        # Handle quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # If animating, skip input handling
        if not is_animating:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and move_cooldown > 100:
                player_game.move(-1, 0)
                move_cooldown = 0

            if keys[pygame.K_RIGHT] and move_cooldown > 100:
                player_game.move(1, 0)
                move_cooldown = 0

            if keys[pygame.K_DOWN]:
                player_game.drop(screen)

            if keys[pygame.K_UP] and move_cooldown > 150:
                player_game.rotateMino()
                move_cooldown = 0

            if fall_time > 500:
                player_game.drop(screen)
                fall_time = 0

        # Check if animations are needed
        boardStateList = get_boardStateList()
        if boardStateList:
            is_animating = True
            display_board_states(screen, player_game)  # Process animation frames
            is_animating = False

        # Always render the text and game board
        text_offset_x = SCREEN_WIDTH + 20
        final_white_points = getWhite()  # Ensure getWhite always returns an integer
        white_cells_earned = final_white_points // 8
        text_to_display = construct_text_to_display(
            player_game, final_white_points, white_cells_earned
        )

        player_game.renderText(
            screen, text=text_to_display, offset_x=text_offset_x, initial_offset_y=20
        )

        player_game.drawGrid(screen, offset_x=0)
        player_game.drawMino(screen, offset_x=0)

        pygame.display.update()

    pygame.quit()



if __name__ == "__main__":
    main()