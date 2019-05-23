# Import packages
import pygame

# Create matrix with all vectors containing elements set to zero.
def create_board():
    board = []
    for row in range(8):
        row = []
        board.append(row)
        for column in range(8):
            column = 0
            row.append(column)
    return board


def place_starting_pieces():
    """Assign starting checker pieces for red and black"""
    # Assign starting board locations for red
    for current_row in range(5, 8, 2):
        for current_column in range(0, 8, 2):
            board[current_row][current_column] = 1
    for current_row in range(6, 7):
        for current_column in range(1, 8, 2):
            board[current_row][current_column] = 1

    # Assign starting board locations for black
    for current_row in range(0, 3, 2):
        for current_column in range(1, 8, 2):
            board[current_row][current_column] = 2
    for current_row in range(1, 2):
        for current_column in range(0, 8, 2):
            board[current_row][current_column] = 2


def is_valid_selection(board, current_player, old_x, old_y):
    """Restricts player from slecting posisitions containing no checker pieces or """
    if board[old_y][old_x] == current_player:
        return True
    elif current_player == 1:
        if board[old_y][old_x] == 3:
            return True
        elif board[old_y][old_x] == 4:
            print("You selected an enemy player's piece. Please select your own piece.")
            return False
        else:
            print("You didn't select a piece. Please try selecting one of your pieces.")
            return False
    else:
        if board[old_y][old_x] == 4:
            return True
        elif board[old_y][old_x] == 3:
            print("You selected an enemy player's piece. Please select your own piece.")
            return False
        else:
            print("You didn't select a piece. Please try selecting one of your pieces.")
            return False

def is_valid_move(current_player, board, old_x, old_y, new_x, new_y):
    """All logic for normal pieces."""
    if board[new_y][new_x] != 0:
        print("You cant land on another piece. Please select another location.")
        return False
    # Checking for valid moves for Player 1
    if board[old_y][old_x] == 1:
        if (new_y - old_y) == -1 and (new_x - old_x) == 1:
            return True
        elif (new_y - old_y) == -1 and (new_x - old_x) == -1:
            return True
        # Checking for valid jump
        elif (new_y - old_y) == -2 and (new_x - old_x) == 2:
            if board[new_y + 1][new_x - 1] == 2 or 4: # Check if jumped piece contains enemey piece
                board[new_y + 1][new_x - 1] = 0 # Eliminate jumped enemy piece
                return True
            else:
                return False
        elif (new_y - old_y) == -2 and (new_x - old_x) == -2:
            if board[new_y + 1][new_x + 1] == 2 or 4: # Check if jumped piece contains enemey piece
                board[new_y + 1][new_x + 1] = 0 # Eliminate jumped enemy piece
                return True
            else:
                return False
    # Checking for valid moves for Player 2
    elif board[old_y][old_x] == 2:
        if (new_y - old_y) == 1 and (new_x - old_x) == 1:
            return True
        elif (new_y - old_y) == 1 and (new_x - old_x) == -1:
            return True
        # Checking for valid jumps for Player 2
        elif (new_y - old_y) == 2 and (new_x - old_x) == 2:
            if board[new_y - 1][new_x - 1] == 1 or 3: # Check if jumped piece contains enemey piece
                board[new_y - 1][new_x - 1] = 0 # Eliminate jumped enemy piece
                return True
            else:
                return False
        elif (new_y - old_y) == 2 and (new_x - old_x) == -2:
            if board[new_y - 1][new_x + 1] == 1 or 3: # Check if jumped piece contains enemey piece
                board[new_y - 1][new_x + 1] = 0 # Eliminate jumped enemy piece
                return True
            else:
                return False
        else:
            print("You can't move that far. Please select another positition to move too.")
            return False

def no_chips_between(board, old_x, old_y, new_x, new_y):
    """Restricts king pieces from jumping over several players at once"""
    board_y_coords = []
    board_x_coords = []
    if old_y < new_y:
        for row in range(old_y, new_y):
            board_y_coords.append(row)
    if old_y > new_y:
        for row in range(old_y, new_y, -1):
            board_y_coords.append(row)
    if old_x < new_x:
        for column in range(old_x, new_x):
            board_x_coords.append(column)
    if old_x > new_x:
        for column in range(old_x, new_x, -1):
            board_x_coords.append(column)

    board_coords = list(zip(board_x_coords, board_y_coords))
    board_values = [board[y][x] for x, y in board_coords]
    if len(board_values) > 2:
        if all(i == 0 for i in board_values[1:-1]) is True:
            board[new_y][new_x] = board[old_y][old_x]
            board[old_y][old_x] = 0
            return True
    if len(board_values) < 2: # Fixes bug where a king could jump over it's own piece if it was a normal jump
        if all(i == 0 for i in board_values[1:]) is True:
            board[new_y][new_x] = board[old_y][old_x]
            board[old_y][old_x] = 0
            return True
    else:
        print("You can't jump over several chips at once. Please try another move.")
        return False

def is_valid_king_move(current_player, board, old_x, old_y, new_x, new_y):
    """All logic for king pieces"""
    # Prevents player from jumping onto another player
    if board[new_y][new_x] != 0:
        print("Even as king you cannot land directly onto another player's piece.")
        return False
    # Prevent horizontal moves
    if new_y == old_y:
        print("Even as a king you cannot move horizontally in this diagonal world.")
        return False

    # Prevent horizontal moves
    if new_x == old_x:
        print("Even as a king you cannot move vertically in this diagonal world.")
        return False

    # Prevent moves that do not have a slope of 1
    if new_x > old_x and new_y > old_y:
        if (new_x - old_x) != (new_y - old_y):
            return False
    if new_x < old_x and new_y < old_y:
        if (old_x - new_x) != (old_y - new_y):
            return False
    if new_x < old_x and new_y > old_y:
        if (old_x - new_x) != (new_y - old_y):
            return False
    if new_x > old_x and new_y < old_y:
        if (new_x - old_x) != (old_y - new_y):
            return False


    # Allow player to move when there are no pieces in between their old position and new position.
    # It exactly the same the is_chips_between function however for the if all statement at the bottom
    # the board_values index extends all the way to new position instead of the -1nth index poistion.
    board_y_coords = []
    board_x_coords = []
    if old_y < new_y:
        for row in range(old_y, new_y):
            board_y_coords.append(row)
    if old_y > new_y:
        for row in range(old_y, new_y, -1):
            board_y_coords.append(row)
    if old_x < new_x:
        for column in range(old_x, new_x):
            board_x_coords.append(column)
    if old_x > new_x:
        for column in range(old_x, new_x, -1):
            board_x_coords.append(column)

    board_coords = list(zip(board_x_coords, board_y_coords))
    board_values = [board[y][x] for x, y in board_coords]
    if all(i == 0 for i in board_values[1:]) is True:
        board[new_y][new_x] = board[old_y][old_x]
        board[old_y][old_x] = 0
        return True


    # Red King Logic
    if board[old_y][old_x] == 3:

        # North East Jump - Delete Enemy
        try:
            if board[new_y + 1][new_x - 1] == 2:
                if old_x < new_x and old_y > new_y:
                    if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                        board[new_y][new_x] = 3
                        board[new_y + 1][new_x - 1] = 0
                        board[old_y][old_x] = 0
                        return True

            if board[new_y + 1][new_x - 1] == 4:
                if old_x < new_x and old_y > new_y:
                    if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                        board[new_y][new_x] = 3
                        board[new_y + 1][new_x - 1] = 0
                        board[old_y][old_x] = 0
        except IndexError:
            pass

        # North West Jump - Delete Enemy
        try:
            if board[new_y + 1][new_x + 1] == 2:
                if old_x > new_x and old_y > new_y:
                    if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                        board[new_y][new_x] = 3
                        board[new_y + 1][new_x + 1] = 0
                        board[old_y][old_x] = 0
                        return True

            if board[new_y + 1][new_x + 1] == 4:
                if old_x > new_x and old_y > new_y:
                    if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                        board[new_y][new_x] = 3
                        board[new_y + 1][new_x + 1] = 0
                        board[old_y][old_x] = 0
                        return True
        except IndexError:
            pass
        # South East Jump - Delete Enemy
        try:
            if board[new_y - 1][new_x - 1] == 2:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x < new_x and old_y < new_y:
                        board[new_y][new_x] = 3
                        board[new_y - 1][new_x - 1] = 0
                        board[old_y][old_x] = 0
                        return True

            if board[new_y - 1][new_x - 1] == 4:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x < new_x and old_y < new_y:
                        board[new_y][new_x] = 3
                        board[new_y - 1][new_x - 1] = 0
                        board[old_y][old_x] = 0
                        return True
        except IndexError:
            pass
        # South West Jump - Delete Enemy
        try:
            if board[new_y - 1][new_x + 1] == 2:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x > new_x and old_y < new_y:
                        board[new_y][new_x] = 3
                        board[new_y - 1][new_x + 1] = 0
                        board[old_y][old_x] = 0
                        return True

            if board[new_y - 1][new_x + 1] == 4:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x > new_x and old_y < new_y:
                        board[new_y][new_x] = 3
                        board[new_y - 1][new_x + 1] = 0
                        board[old_y][old_x] = 0
                        return True
        except IndexError:
            pass


    # Black King Logic
    if board[old_y][old_x] == 4:

        # North East Jump - Delete Enemy
        try:
            if board[new_y + 1][new_x - 1] == 1:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x < new_x and old_y > new_y:
                        board[new_y][new_x] = 4
                        board[new_y + 1][new_x - 1] = 0
                        board[old_y][old_x] = 0
                        return True

            elif board[new_y + 1][new_x - 1] == 3:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x < new_x and old_y > new_y:
                        board[new_y][new_x] = 4
                        board[new_y + 1][new_x - 1] = 0
                        board[old_y][old_x] = 0
                        return True
        except IndexError:
            pass

    #     North West Jump - Delete Enemy
        try:
            if board[new_y + 1][new_x + 1] == 1:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x > new_x and old_y > new_y:
                        board[new_y][new_x] = 4
                        board[new_y + 1][new_x + 1] = 0
                        board[old_y][old_x] = 0
                        return True

            elif board[new_y + 1][new_x + 1] == 3:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x > new_x and old_y > new_y:
                        board[new_y][new_x] = 4
                        board[new_y + 1][new_x + 1] = 0
                        board[old_y][old_x] = 0
                        return True
        except IndexError:
            pass

        # South East Jump - Delete Enemy
        try:
            if board[new_y - 1][new_x - 1] == 1:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x < new_x and old_y < new_y:
                        board[new_y][new_x] = 4
                        board[new_y - 1][new_x - 1] = 0
                        board[old_y][old_x] = 0
                        return True

            elif board[new_y - 1][new_x - 1] == 3:
                if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                    if old_x < new_x and old_y < new_y:
                        board[new_y][new_x] = 4
                        board[new_y - 1][new_x - 1] = 0
                        board[old_y][old_x] = 0
                        return True
        except IndexError:
            pass

        # South West Jump - Delete Enemy
        try:
            if board[new_y - 1][new_x + 1] == 1:
                if old_x > new_x and old_y < new_y:
                    if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                        board[new_y][new_x] = 4
                        board[new_y - 1][new_x + 1] = 0
                        board[old_y][old_x] = 0
                        return True

            elif board[new_y - 1][new_x + 1] == 3:
                if old_x > new_x and old_y < new_y:
                    if no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                        board[new_y][new_x] = 4
                        board[new_y - 1][new_x + 1] = 0
                        board[old_y][old_x] = 0
                        return True
        except IndexError:
            pass


def check_for_win(board):
    remaining_red_pieces = []
    for row in board:
        remaining_red_pieces.append(row.count(1))
        remaining_red_pieces.append(row.count(3))
    if sum(remaining_red_pieces) == 0:
        print("Black has won!")
        return True
        
    remaining_black_pieces = []
    for row in board:
        remaining_black_pieces.append(row.count(2))
        remaining_black_pieces.append(row.count(4))
    if sum(remaining_black_pieces) == 0:
        print("Red has won!")
        return True

# Initalize vairables
game_over = False
board = create_board()
place_starting_pieces()

# Initalize pygame
pygame.init()

# Set the height and width of the screen
window_size = [600, 600]
screen = pygame.display.set_mode(window_size)

# Set title of screen
pygame.display.set_caption("Checkers")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
dark_red = (139 , 0, 0)
grey = (128, 128, 128)
gold = (255, 215, 0)

# This sets the width, height and margin of each board cell
window_width = window_size[0]
window_height = window_size[1]
total_rows = 8
total_columns = 8
width = (window_width // total_columns)
height = (window_height // total_rows)

# Set the radius and border border of each checker piece
radius = (window_width // 20)
border = (window_width // 200)

# Current player turn
current_player = 1
print("Red's Turn") # Printing at start of the game before main loop

# Main active game loop
while not done:
    for event in pygame.event.get():  # User did something
        mouse_pos = pygame.mouse.get_pos()
        mouse_matrix_pos = ((mouse_pos[0] // width), (mouse_pos[1] // height)) # Matrix Cordinates of Mouse posisiton
        # print(mouse_matrix_pos)
        
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        elif event.type == pygame.MOUSEBUTTONDOWN:
            current_pos = pygame.mouse.get_pos()
            # Translating mouse x, y screen coordinates to matrix coordinates
            old_x = (current_pos[0] // width)
            old_y = (current_pos[1] // height)
            # print(f"Old coordinates: [{old_x}, {old_y}]")

            if is_valid_selection(board, current_player, old_x, old_y) == True:
                pass # Do nothing if player has made a valid selection
            else:
                continue # Looping indefintely until a valid choice has been selected by the current player

            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    new_pos = pygame.mouse.get_pos()
                    # Translating mouse x, y screen coordinates to matrix coordinates
                    new_x = (new_pos[0] // width)
                    new_y = (new_pos[1] // height)
                    # print(f"New coordinates: [{new_x}, {new_y}]")

                    if is_valid_move(current_player, board, old_x, old_y, new_x, new_y) == True:
                        board[new_y][new_x] = current_player # Set new coordinates to player value
                        board[old_y][old_x] = 0 # Set old coordinates to 0

                        if check_for_win(board) == True:
                            done = True
                    
                        # Alternate player turn
                        if current_player == 1:
                            current_player = 2
                            print("Black's Turn")
                        else:
                            current_player = 1
                            print("Red's Turn")

                    # Red King Check
                    elif board[old_y][old_x] == 3:
                        if is_valid_king_move(current_player, board, old_x, old_y, new_x, new_y) == True:

                            if check_for_win(board) == True:
                                done = True
                        
                            # Alternate player turn
                            if current_player == 1:
                                current_player = 2
                                print("Black's Turn")
                            else:
                                current_player = 1
                                print("Red's Turn")

                    # Black King Check
                    elif board[old_y][old_x] == 4:
                        if is_valid_king_move(current_player, board, old_x, old_y, new_x, new_y) == True:

                            if check_for_win(board) == True:
                                done = True
                        
                            # Alternate player turn
                            if current_player == 1:
                                current_player = 2
                                print("Black's Turn")
                            else:
                                current_player = 1
                                print("Red's Turn")

                    else:
                        break

                    # Turn player into king if they make it to the opposite side of the board
                    for row in range(8):
                        for column in range(8):
                            # Checking for player 1 king pieces
                            if board[0][column] == 1:
                                board[0][column] = 3
                             # Cecking for player 2 king pieces
                            elif board[7][column] == 2:
                                board[7][column] = 4
                    break

    # Draw onto screen
    for row in range(8):
        for column in range(8):
            #  Variables for pygame.draw pos paramater
            # Draw all grid locations as either white or black rectangle
            if (row + column) % 2 == 0:
                color = white
            else:
                color = black
            rect = pygame.draw.rect(screen, color, [width * column, height * row, width, height])
            rect_center = rect.center
            if board[row][column] == 1:
                pygame.draw.circle(screen, red, rect_center, radius)
            if board[row][column] == 2:
                pygame.draw.circle(screen, black, rect_center, radius)
                # Draw border around black pieces so that they're visible
                pygame.draw.circle(screen, grey, rect_center, radius, border)
            # Drawing king pieces borders
            if board[row][column] == 3:
                pygame.draw.circle(screen, red, rect_center, radius)
                pygame.draw.circle(screen, gold, rect_center, radius, border)
            if board[row][column] == 4:
                pygame.draw.circle(screen, gold, rect_center, radius, border)

    # Limit to 60 frames per second
    clock.tick(60)

    # Update screen with what we drew
    pygame.display.flip()

# Exit the game
pygame.quit()
