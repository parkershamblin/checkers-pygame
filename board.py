import pygame
from constants import (
    BOARD_BLACK,
    BOARD_WHITE,
    BLACK,
    BLACK_COLOR,
    BLACK_KING,
    BLACK_PAWN,
    CELL_HEIGHT,
    CELL_WIDTH,
    EMPTY,
    GOLD,
    GREY,
    PLAYER_NAMES,
    PLAYER_PIECES,
    PLAYER_KINGS,
    PLAYER_PAWNS,
    RED,
    RED_COLOR,
    RED_KING,
    RED_PAWN,
    ROWS,
    SELECTED_GREEN,
    PIECE_BORDER,
    PIECE_RADIUS,
    COLUMNS,
)


class Board:
    PLAYER_PIECES = PLAYER_PIECES
    PLAYER_NAMES = PLAYER_NAMES
    PLAYER_KINGS = PLAYER_KINGS
    PLAYER_PAWNS = PLAYER_PAWNS
    RED_PAWN = RED_PAWN
    BLACK_PAWN = BLACK_PAWN
    RED_KING = RED_KING
    BLACK_KING = BLACK_KING
    RED = RED
    BLACK = BLACK
    ROWS = ROWS
    COLUMNS = COLUMNS
    CELL_WIDTH = CELL_WIDTH
    CELL_HEIGHT = CELL_HEIGHT
    PIECE_RADIUS = PIECE_RADIUS
    PIECE_BORDER = PIECE_BORDER

    def __init__(self):
        self._board = self._create_board()
        self._place_starting_pieces()
        self._current_player = RED
        self._selected_square = None
        self._must_continue_from = None
        self._game_over = False

    # Properties for accessing private attributes
    @property
    def board(self):
        return self._board

    @property
    def current_player(self):
        return self._current_player

    @property
    def selected_square(self):
        return self._selected_square

    @property
    def must_continue_from(self):
        return self._must_continue_from

    @property
    def game_over(self):
        return self._game_over

    def _create_board(self):
        """Create an empty checkers board."""
        return [[EMPTY for column in range(self.COLUMNS)] for row in range(self.ROWS)]

    def _place_starting_pieces(self):
        """Assign starting checker pieces for red and black."""
        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                if (row + column) % 2 == 1:
                    if row < 3:
                        self._board[row][column] = BLACK_PAWN
                    elif row > 4:
                        self._board[row][column] = RED_PAWN

    def is_on_board(self, x, y):
        return 0 <= x < self.COLUMNS and 0 <= y < self.ROWS

    def get_opponent(self, player):
        return BLACK if player == RED else RED

    def get_piece_owner(self, piece):
        if piece in self.PLAYER_PIECES[RED]:
            return RED
        if piece in self.PLAYER_PIECES[BLACK]:
            return BLACK
        return None

    def is_king(self, piece):
        return piece in (self.RED_KING, self.BLACK_KING)

    def get_move_directions(self, piece, player):
        if self.is_king(piece):
            return ((-1, -1), (1, -1), (-1, 1), (1, 1))

        forward = -1 if player == RED else 1
        return ((-1, forward), (1, forward))

    def _is_valid_selection(self, x, y):
        """Return True when the selected square contains the current player's piece."""
        if not self.is_on_board(x, y):
            print("That square is outside the board.")
            return False

        if self._must_continue_from is not None and (x, y) != self._must_continue_from:
            print("You must continue jumping with the same piece.")
            return False

        piece = self._board[y][x]
        if piece in PLAYER_PIECES[self._current_player]:
            return True

        if piece == EMPTY:
            print("You didn't select a piece. Please select one of your pieces.")
        else:
            print("You've selected the other player's piece. Please select your own piece.")
        return False

    def _get_move_details(self, old_x, old_y, new_x, new_y):
        """Validate a move and return (is_valid, captured_square, promoted, message)."""
        if not self.is_on_board(old_x, old_y) or not self.is_on_board(new_x, new_y):
            return False, None, False, "That move goes outside the board."

        piece = self._board[old_y][old_x]
        if piece not in PLAYER_PIECES[self._current_player]:
            return False, None, False, "Please move one of your own pieces."

        if self._board[new_y][new_x] != EMPTY:
            return False, None, False, "You cannot land on another piece."

        dx = new_x - old_x
        dy = new_y - old_y
        if abs(dx) != abs(dy) or dx == 0:
            return False, None, False, "Pieces must move diagonally."

        directions = self.get_move_directions(piece, self._current_player)
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

        if (step_x, step_y) not in directions:
            return False, None, False, "Pawns can only move forward."

        if abs(dx) == 1:
            return True, None, self._will_promote(piece, new_y), ""

        if abs(dx) == 2:
            middle_x = old_x + step_x
            middle_y = old_y + step_y
            jumped_piece = self._board[middle_y][middle_x]
            if self.get_piece_owner(jumped_piece) == self.get_opponent(self._current_player):
                return True, (middle_x, middle_y), self._will_promote(piece, new_y), ""
            return False, None, False, "You can only jump over the other player's piece."

        return False, None, False, "Pieces can only move one space or jump one piece."

    def _will_promote(self, piece, y):
        return (piece == RED_PAWN and y == 0) or (piece == BLACK_PAWN and y == self.ROWS - 1)

    def _promote_piece(self, x, y):
        if self._board[y][x] == RED_PAWN and y == 0:
            self._board[y][x] = RED_KING
            return True
        if self._board[y][x] == BLACK_PAWN and y == self.ROWS - 1:
            self._board[y][x] = BLACK_KING
            return True
        return False

    def _move_piece(self, old_x, old_y, new_x, new_y):
        """Apply a move if valid and return (moved, captured, promoted)."""
        is_valid, captured_square, promoted, message = self._get_move_details(old_x, old_y, new_x, new_y)
        if not is_valid:
            print(message)
            return False, False, False

        self._board[new_y][new_x] = self._board[old_y][old_x]
        self._board[old_y][old_x] = EMPTY

        captured = captured_square is not None
        if captured:
            captured_x, captured_y = captured_square
            self._board[captured_y][captured_x] = EMPTY

        promoted = self._promote_piece(new_x, new_y) or promoted
        return True, captured, promoted

    def _has_capture_from(self, x, y):
        if not self.is_on_board(x, y):
            return False

        piece = self._board[y][x]
        if piece not in PLAYER_PIECES[self._current_player]:
            return False

        for step_x, step_y in self.get_move_directions(piece, self._current_player):
            middle_x = x + step_x
            middle_y = y + step_y
            landing_x = x + (step_x * 2)
            landing_y = y + (step_y * 2)

            if not self.is_on_board(landing_x, landing_y):
                continue

            jumped_piece = self._board[middle_y][middle_x]
            if self._board[landing_y][landing_x] == EMPTY and self.get_piece_owner(jumped_piece) == self.get_opponent(self._current_player):
                return True

        return False

    def _has_any_legal_move(self, player):
        for y in range(self.ROWS):
            for x in range(self.COLUMNS):
                piece = self._board[y][x]
                if piece not in PLAYER_PIECES[player]:
                    continue

                for step_x, step_y in self.get_move_directions(piece, player):
                    move_x = x + step_x
                    move_y = y + step_y
                    jump_x = x + (step_x * 2)
                    jump_y = y + (step_y * 2)

                    if self.is_on_board(move_x, move_y) and self._board[move_y][move_x] == EMPTY:
                        return True

                    middle_x = x + step_x
                    middle_y = y + step_y
                    if (self.is_on_board(jump_x, jump_y)
                        and self.is_on_board(middle_x, middle_y)
                        and self._board[jump_y][jump_x] == EMPTY
                        and self.get_piece_owner(self._board[middle_y][middle_x]) == self.get_opponent(player)
                    ):
                        return True

        return False

    def _has_player_pieces(self, player):
        return any(piece in PLAYER_PIECES[player] for row in self._board for piece in row)

    def _check_for_win(self):
        opponent = self.get_opponent(self._current_player)
        if not self._has_player_pieces(opponent):
            print(f"{PLAYER_NAMES[self._current_player]} has won by capturing all pieces!")
            return True

        if not self._has_any_legal_move(opponent):
            print(f"{PLAYER_NAMES[self._current_player]} has won because {PLAYER_NAMES[opponent]} has no legal moves!")
            return True

        return False

    def _board_position_from_mouse(self, mouse_pos):
        return mouse_pos[0] // CELL_WIDTH, mouse_pos[1] // CELL_HEIGHT

    def _switch_turns(self):
        self._current_player = self.get_opponent(self._current_player)
        print(f"{PLAYER_NAMES[self._current_player]}'s Turn")

    def handle_mouse_down(self, mouse_pos):
        x, y = self._board_position_from_mouse(mouse_pos)
        if self._is_valid_selection(x, y):
            self._selected_square = (x, y)

    def handle_mouse_up(self, mouse_pos):
        if self._selected_square is None or self._game_over:
            return

        old_x, old_y = self._selected_square
        new_x, new_y = self._board_position_from_mouse(mouse_pos)
        self._selected_square = None

        moved, captured, promoted = self._move_piece(old_x, old_y, new_x, new_y)
        if not moved:
            return

        if self._check_for_win():
            self._game_over = True
            return

        if captured and not promoted and self._has_capture_from(new_x, new_y):
            self._must_continue_from = (new_x, new_y)
            self._selected_square = self._must_continue_from
            print("You can jump again with the same piece.")
        else:
            self._must_continue_from = None
            self._switch_turns()

    def draw(self, screen):
        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                square_color = BOARD_WHITE if (row + column) % 2 == 0 else BOARD_BLACK
                rect = pygame.draw.rect(
                    screen,
                    square_color,
                    [CELL_WIDTH * column, CELL_HEIGHT * row, CELL_WIDTH, CELL_HEIGHT],
                )

                if self._selected_square == (column, row):
                    pygame.draw.rect(screen, SELECTED_GREEN, rect, PIECE_BORDER * 2)

                rect_center = rect.center
                piece = self._board[row][column]
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