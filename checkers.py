# Import packages
import pygame


# Piece values
EMPTY = 0
RED_PAWN = 1
BLACK_PAWN = 2
RED_KING = 3
BLACK_KING = 4

# Player values
RED = 1
BLACK = 2

# Board size
ROWS = 8
COLUMNS = 8

# Display settings
WINDOW_SIZE = (600, 600)
CELL_WIDTH = WINDOW_SIZE[0] // COLUMNS
CELL_HEIGHT = WINDOW_SIZE[1] // ROWS
PIECE_RADIUS = WINDOW_SIZE[0] // 20
PIECE_BORDER = max(1, WINDOW_SIZE[0] // 200)

# Colors
BOARD_BLACK = (0, 0, 0)
BOARD_WHITE = (255, 255, 255)
RED_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
GREY = (128, 128, 128)
GOLD = (255, 215, 0)
SELECTED_GREEN = (0, 180, 0)

PLAYER_NAMES = {
    RED: "Red",
    BLACK: "Black",
}

PLAYER_PAWNS = {
    RED: RED_PAWN,
    BLACK: BLACK_PAWN,
}

PLAYER_KINGS = {
    RED: RED_KING,
    BLACK: BLACK_KING,
}

PLAYER_PIECES = {
    RED: (RED_PAWN, RED_KING),
    BLACK: (BLACK_PAWN, BLACK_KING),
}


def create_board():
    """Create an empty checkers board."""
    return [[EMPTY for column in range(COLUMNS)] for row in range(ROWS)]


def place_starting_pieces(board):
    """Assign starting checker pieces for red and black."""
    for row in range(ROWS):
        for column in range(COLUMNS):
            if (row + column) % 2 == 1:
                if row < 3:
                    board[row][column] = BLACK_PAWN
                elif row > 4:
                    board[row][column] = RED_PAWN


def is_on_board(x, y):
    return 0 <= x < COLUMNS and 0 <= y < ROWS


def get_opponent(player):
    return BLACK if player == RED else RED


def get_piece_owner(piece):
    if piece in PLAYER_PIECES[RED]:
        return RED
    if piece in PLAYER_PIECES[BLACK]:
        return BLACK
    return None


def is_king(piece):
    return piece in (RED_KING, BLACK_KING)


def get_move_directions(piece, player):
    if is_king(piece):
        return ((-1, -1), (1, -1), (-1, 1), (1, 1))

    forward = -1 if player == RED else 1
    return ((-1, forward), (1, forward))


def is_valid_selection(board, current_player, x, y, must_continue_from=None):
    """Return True when the selected square contains the current player's piece."""
    if not is_on_board(x, y):
        print("That square is outside the board.")
        return False

    if must_continue_from is not None and (x, y) != must_continue_from:
        print("You must continue jumping with the same piece.")
        return False

    piece = board[y][x]
    if piece in PLAYER_PIECES[current_player]:
        return True

    if piece == EMPTY:
        print("You didn't select a piece. Please select one of your pieces.")
    else:
        print("You've selected the other player's piece. Please select your own piece.")
    return False


def get_move_details(board, current_player, old_x, old_y, new_x, new_y):
    """Validate a move and return (is_valid, captured_square, promoted, message)."""
    if not is_on_board(old_x, old_y) or not is_on_board(new_x, new_y):
        return False, None, False, "That move goes outside the board."

    piece = board[old_y][old_x]
    if piece not in PLAYER_PIECES[current_player]:
        return False, None, False, "Please move one of your own pieces."

    if board[new_y][new_x] != EMPTY:
        return False, None, False, "You cannot land on another piece."

    dx = new_x - old_x
    dy = new_y - old_y
    if abs(dx) != abs(dy) or dx == 0:
        return False, None, False, "Pieces must move diagonally."

    directions = get_move_directions(piece, current_player)
    step_x = 1 if dx > 0 else -1
    step_y = 1 if dy > 0 else -1

    if (step_x, step_y) not in directions:
        return False, None, False, "Pawns can only move forward."

    if abs(dx) == 1:
        return True, None, will_promote(piece, new_y), ""

    if abs(dx) == 2:
        middle_x = old_x + step_x
        middle_y = old_y + step_y
        jumped_piece = board[middle_y][middle_x]
        if get_piece_owner(jumped_piece) == get_opponent(current_player):
            return True, (middle_x, middle_y), will_promote(piece, new_y), ""
        return False, None, False, "You can only jump over the other player's piece."

    return False, None, False, "Pieces can only move one space or jump one piece."


def will_promote(piece, y):
    return (piece == RED_PAWN and y == 0) or (piece == BLACK_PAWN and y == ROWS - 1)


def promote_piece(board, x, y):
    if board[y][x] == RED_PAWN and y == 0:
        board[y][x] = RED_KING
        return True
    if board[y][x] == BLACK_PAWN and y == ROWS - 1:
        board[y][x] = BLACK_KING
        return True
    return False


def move_piece(board, current_player, old_x, old_y, new_x, new_y):
    """Apply a move if valid and return (moved, captured, promoted)."""
    is_valid, captured_square, promoted, message = get_move_details(
        board,
        current_player,
        old_x,
        old_y,
        new_x,
        new_y,
    )
    if not is_valid:
        print(message)
        return False, False, False

    board[new_y][new_x] = board[old_y][old_x]
    board[old_y][old_x] = EMPTY

    captured = captured_square is not None
    if captured:
        captured_x, captured_y = captured_square
        board[captured_y][captured_x] = EMPTY

    promoted = promote_piece(board, new_x, new_y) or promoted
    return True, captured, promoted


def has_capture_from(board, current_player, x, y):
    if not is_on_board(x, y):
        return False

    piece = board[y][x]
    if piece not in PLAYER_PIECES[current_player]:
        return False

    for step_x, step_y in get_move_directions(piece, current_player):
        middle_x = x + step_x
        middle_y = y + step_y
        landing_x = x + (step_x * 2)
        landing_y = y + (step_y * 2)

        if not is_on_board(landing_x, landing_y):
            continue

        jumped_piece = board[middle_y][middle_x]
        if board[landing_y][landing_x] == EMPTY and get_piece_owner(jumped_piece) == get_opponent(current_player):
            return True

    return False


def has_any_legal_move(board, current_player):
    for y in range(ROWS):
        for x in range(COLUMNS):
            piece = board[y][x]
            if piece not in PLAYER_PIECES[current_player]:
                continue

            for step_x, step_y in get_move_directions(piece, current_player):
                move_x = x + step_x
                move_y = y + step_y
                jump_x = x + (step_x * 2)
                jump_y = y + (step_y * 2)

                if is_on_board(move_x, move_y) and board[move_y][move_x] == EMPTY:
                    return True

                if is_on_board(jump_x, jump_y) and has_capture_from(board, current_player, x, y):
                    return True

    return False


def has_player_pieces(board, player):
    return any(piece in PLAYER_PIECES[player] for row in board for piece in row)


def check_for_win(current_player, board):
    opponent = get_opponent(current_player)
    if not has_player_pieces(board, opponent):
        print(f"{PLAYER_NAMES[current_player]} has won by capturing all pieces!")
        return True

    if not has_any_legal_move(board, opponent):
        print(f"{PLAYER_NAMES[current_player]} has won because {PLAYER_NAMES[opponent]} has no legal moves!")
        return True

    return False


def board_position_from_mouse(mouse_pos):
    return mouse_pos[0] // CELL_WIDTH, mouse_pos[1] // CELL_HEIGHT


def switch_turns(current_player):
    next_player = get_opponent(current_player)
    print(f"{PLAYER_NAMES[next_player]}'s Turn")
    return next_player


def draw_board(screen, board, selected_square=None):
    for row in range(ROWS):
        for column in range(COLUMNS):
            square_color = BOARD_WHITE if (row + column) % 2 == 0 else BOARD_BLACK
            rect = pygame.draw.rect(
                screen,
                square_color,
                [CELL_WIDTH * column, CELL_HEIGHT * row, CELL_WIDTH, CELL_HEIGHT],
            )

            if selected_square == (column, row):
                pygame.draw.rect(screen, SELECTED_GREEN, rect, PIECE_BORDER * 2)

            rect_center = rect.center
            piece = board[row][column]
            if piece == RED_PAWN:
                pygame.draw.circle(screen, RED_COLOR, rect_center, PIECE_RADIUS)
            elif piece == BLACK_PAWN:
                pygame.draw.circle(screen, BLACK_COLOR, rect_center, PIECE_RADIUS)
                pygame.draw.circle(screen, GREY, rect_center, PIECE_RADIUS, PIECE_BORDER)
            elif piece == RED_KING:
                pygame.draw.circle(screen, RED_COLOR, rect_center, PIECE_RADIUS)
                pygame.draw.circle(screen, GOLD, rect_center, PIECE_RADIUS, PIECE_BORDER)
            elif piece == BLACK_KING:
                pygame.draw.circle(screen, BLACK_COLOR, rect_center, PIECE_RADIUS)
                pygame.draw.circle(screen, GOLD, rect_center, PIECE_RADIUS, PIECE_BORDER)


def main():
    board = create_board()
    place_starting_pieces(board)

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Checkers")
    clock = pygame.time.Clock()

    current_player = RED
    selected_square = None
    must_continue_from = None
    game_over = False

    print(f"{PLAYER_NAMES[current_player]}'s Turn")

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = board_position_from_mouse(pygame.mouse.get_pos())
                if is_valid_selection(board, current_player, x, y, must_continue_from):
                    selected_square = (x, y)

            elif event.type == pygame.MOUSEBUTTONUP and selected_square is not None:
                old_x, old_y = selected_square
                new_x, new_y = board_position_from_mouse(pygame.mouse.get_pos())
                selected_square = None

                moved, captured, promoted = move_piece(board, current_player, old_x, old_y, new_x, new_y)
                if not moved:
                    continue

                if check_for_win(current_player, board):
                    game_over = True
                    continue

                if captured and not promoted and has_capture_from(board, current_player, new_x, new_y):
                    must_continue_from = (new_x, new_y)
                    selected_square = must_continue_from
                    print("You can jump again with the same piece.")
                else:
                    must_continue_from = None
                    current_player = switch_turns(current_player)

        draw_board(screen, board, selected_square)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
