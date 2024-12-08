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

def analyze_board_states(boardStateList):
    """Analyze the board states and track changes."""
    changeTracker = []

    for i in range(1, len(boardStateList)):
        prev_board = boardStateList[i - 1]
        curr_board = boardStateList[i]

        # Identify non-matching cells
        non_matching_cells = []
        for y in range(len(curr_board)):
            for x in range(len(curr_board[0])):
                if prev_board[y][x] != curr_board[y][x]:
                    non_matching_cells.append((y, x))

        # Analyze non-matching cells
        if len(non_matching_cells) == 1:
            y, x = non_matching_cells[0]
            prev_cell = prev_board[y][x]
            curr_cell = curr_board[y][x]
            if prev_cell[:4] != "0000" and curr_cell[:4] == "0000":
                changeTracker.append(f"E{prev_cell[2:4]}")  # Data erase
            elif prev_cell[1] == "C" and curr_cell[1] == "S":
                changeTracker.append(f"S{prev_cell[2:4]}")  # Shape change
        elif len(non_matching_cells) == 2:
            changeTracker.append("P00")  # Position change

    changeTracker.append("000")

    # Create a list of indexes where neighboring values in changeTracker differ
    changeList = []
    for i in range(len(changeTracker) - 1):
        if changeTracker[i] != changeTracker[i + 1]:
            changeList.append(i + 1)

    # Calculate points based on changeTracker
    points_earned = 0
    e_count = 0

    for i in range(len(changeTracker)):
        if changeTracker[i][0] == "E":
            e_count += 1
            if e_count > 8:
                points_earned += 2  # Double points for E changes after the 8th
            else:
                points_earned += 1

    for index in changeList:
        if index < len(changeTracker) and changeTracker[index][0] == "S":
            points_earned += 1  # Add 1 point for each critical S change

    # Check if the final board state is completely `0000-00` and the second-to-last frame contains at least one "W"
    if all(cell[:4] == "0000" for row in boardStateList[-1] for cell in row) and \
       any(cell[0] == "W" for row in boardStateList[0] for cell in row):
        setWhite(0)
        points_earned = 0

    return changeTracker, changeList, points_earned

def display_board_states(screen, game):
    """Displays the progression of board states in `boardStateList` with scoring."""
    boardStateList = get_boardStateList()
    if not boardStateList or len(boardStateList) <= 2:
        return

    _, changeList, points_earned = analyze_board_states(boardStateList)

    # Update the white points earned
    setWhite(getWhite() + points_earned)

    # Display all board states in order
    for i, board_state in enumerate(boardStateList):
        redraw_game_state(screen, game, board_state)
        if i == 0:
            pygame.time.delay(500)  # First state lasts 0.5 seconds
        else:
            pygame.time.delay(150)  # Subsequent states last 0.15 seconds

    # Display key frames from changeList twice
    for _ in range(2):
        for index in changeList:
            if index < len(boardStateList):  # Ensure index is within bounds
                redraw_game_state(screen, game, boardStateList[index])
                pygame.time.delay(250)  # Display for 0.25 seconds

            # Handle quitting the game during animation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    set_boardStateList([])  # Clear the list after analysis

    # Remove the current tetrimino block and spawn a new one
    game.forceSpawnNewMino()

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