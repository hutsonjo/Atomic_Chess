# Author: Joshua Hutson
# GitHub username: hutsonjo
# Date: 5/27/2024
# Description: The program runs a game of atomic chess. The players start the game by creating a ChessVar object
#              and then taking turns by entering their starting position and desired landing position  as parameters
#              with the make_move function. Standard Atomic Chess rules apply, but with the exclusion of check,
#              checkmate, en passant, castling and pawn promotion. If a move is not legal, the make_move function will
#              return False and thus, to continue the game, that player must try a new move.

class ChessVar:
    """A game of atomic chess that is defined by whose turn it is, the state of the game, and which positions are on the
    board. Contains methods for determining the game state, printing the board, and making a move. Also contains methods
    for move validation, checking for king presence, and altering the board upon capture."""

    def __init__(self):
        """Initialize the game of Atomic Chess that is defined by whose turn it is, the state of the game, and the state
        of the board."""
        self._turn = "WHITE"
        self._game_state = "UNFINISHED"
        self._board = [["WR", "WP", '00', '00', '00', '00', "BP", "BR"],
                       ["WN", "WP", '00', '00', '00', '00', "BP", "BN"],
                       ["WI", "WP", '00', '00', '00', '00', "BP", "BI"],
                       ["WQ", "WP", '00', '00', '00', '00', "BP", "BQ"],
                       ["WK", "WP", '00', '00', '00', '00', "BP", "BK"],
                       ["WI", "WP", '00', '00', '00', '00', "BP", "BI"],
                       ["WN", "WP", '00', '00', '00', '00', "BP", "BN"],
                       ["WR", "WP", '00', '00', '00', '00', "BP", "BR"]
                       ]

    def get_game_state(self):
        """Returns the state of the game to the user, notifying them if the game has finished or not and who has won
        if it has."""
        return self._game_state

    def print_board(self):
        """Prints out a visual representation of the game board and writes an end of line sequence."""
        letters = "abcdefgh"
        print('    1     2     3     4     5     6     7     8')
        for i in range(0, 8):
            print(f'{letters[i]} {self._board[i]}')

    def make_move(self, start_pos: str, end_pos: str) -> bool:
        """Moves a chess piece on the board from one position to another, calling to other functions to determine if the
        move is valid, to alter the board if there is a capture. Alters the board itself if a move is valid but there is
        no capture.

        Args: start_pos: A string representing the starting position of the piece to be moved.
            end_pos: A string representing the ending position of the piece to be moved.

        Returns: A boolean value that signifies if the move is valid and that the board has therefore been changed as
            well as whose turn it is.
        """
        if self._game_state != 'UNFINISHED':  # Does not allow play on a game that is finished.
            return False

        # Ensure that the row position is within range
        letters = "abcdefgh"
        if start_pos[0] not in letters or end_pos[0] not in letters:
            return False

        # Initialize a value for the piece that is to be moved and the index of the row and column of this space.
        start_row = letters.index(start_pos[0])
        start_col = int(start_pos[1]) - 1
        if 0 > start_row or 0 > start_col:  # Ensures that the values are within range.
            return False
        if 7 < start_row or 7 < start_col:  # Ensures that the values are within range.
            return False
        moving_piece = self._board[start_row][start_col]

        # Initialize the value for what the landing target contains and the index of the row and column of this space.
        end_row = letters.index(end_pos[0])
        end_col = int(end_pos[1]) - 1
        if 0 > end_row or 0 > end_col:  # Ensures that the values are within range.
            return False
        if 7 < end_row or 7 < end_col:  # Ensures that the values are within range.
            return False
        landing_space = self._board[end_row][end_col]

        # Determines if the move is valid and if so, will there be a capture. The board is updated accordingly.
        validity = self.validate_move(moving_piece, start_row, start_col, landing_space, end_row, end_col)
        if validity:
            if landing_space != '00':  # A capture has occurred
                atomic = self.atomic_landing(end_row, end_col)
                if not atomic:
                    return False  # function returns False only if a move will destroy both kings

            else:  # Move is legal, but no capture occurred
                self._board[end_row][end_col] = moving_piece
            self._board[start_row][start_col] = '00'

            # Modifies the turn after a legal move was played
            if self._turn == "WHITE":
                self._turn = "BLACK"
            else:
                self._turn = "WHITE"

            return True
        else:
            return False

    def validate_move(self, moving_piece: str, start_row: int, start_col: int, landing_space: str, end_row: int,
                      end_col: int) -> bool:
        """Validates whether the move is legal by evaluating the piece being moved, its final location, and whose
        turn it currently is. A separate function is called to determine if the move is legal for each specific piece.

        Args: moving_piece: A string representing the piece being moved.
            start_row: An integer representing the starting row of the moving piece.
            start_col: An integer representing the starting column of the moving piece.
            landing_space: A string representing the value of the intended landing space of the moving piece.
            end_row: An integer representing the starting row of the landing space.
            end_col: An integer representing the starting column of the landing space.

        Returns: A boolean value that signifies if the move is valid.
        """
        if moving_piece == '00':  # Declares move invalid if there is no piece to move
            return False
        if start_row == end_row and start_col == end_col:  # Declares move invalid if there is no movement
            return False

        if self._turn == "WHITE" and "B" in moving_piece:  # Invalidates black going on white's turn
            return False
        if self._turn == "WHITE" and "W" in landing_space:  # Invalidates direct friendly captures for white
            return False

        if self._turn == "BLACK" and "W" in moving_piece:  # Invalidates white going on black's turn
            return False
        if self._turn == "BLACK" and "B" in landing_space:  # Invalidates direct friendly captures for black
            return False

        # A series of checks to evaluate what piece is being moved. A second validation call will verify the movement
        #   for that particular piece.
        if "P" in moving_piece:
            return self.validate_pawn(start_row, start_col, landing_space, end_row, end_col)

        if "R" in moving_piece:
            return self.validate_rook(start_row, start_col, end_row, end_col)

        if "N" in moving_piece:
            return self.validate_knight(start_row, start_col, end_row, end_col)

        if "I" in moving_piece:
            return self.validate_bishop(start_row, start_col, end_row, end_col)

        if "Q" in moving_piece:
            return self.validate_queen(start_row, start_col, end_row, end_col)

        if "K" in moving_piece:
            return self.validate_king(start_row, start_col, landing_space, end_row, end_col)

    def validate_pawn(self, start_row: int, start_col: int, landing_space: str, end_row: int, end_col: int) -> bool:
        """validates whether the move is legal specifically for the pawn.

        Args: start_row: An integer representing the starting row of the moving piece.
            start_col: An integer representing the starting column of the moving piece.
            landing_space: A string representing the value of the intended landing space of the moving piece.
            end_row: An integer representing the starting row of the landing space.
            end_col: An integer representing the starting column of the landing space.

        Returns: A boolean value that signifies if the move is valid.
        """
        # Rules to allow White to move a pawn two spaces on the first turn.
        if start_col == 1 and start_row == end_row and self._turn == "WHITE":
            if start_col + 1 == end_col or start_col + 2 == end_col:
                if landing_space == '00':
                    return True

        # Rules to allow Black to move a pawn two spaces on the first turn.
        elif start_col == 6 and start_row == end_row and self._turn == "BLACK":
            if start_col - 1 == end_col or start_col - 2 == end_col:
                if landing_space == '00':
                    return True

        # Rules for standard non-capture white pawn movement.
        elif start_row == end_row and self._turn == "WHITE":
            if start_col + 1 == end_col:
                if landing_space == '00':
                    return True

        # Rules for standard non-capture black pawn movement.
        elif start_row == end_row and self._turn == "BLACK":
            if start_col - 1 == end_col:
                if landing_space == '00':
                    return True

        # Rules for capture movement of pawns for both players.
        elif abs(start_row - end_row) == 1:
            if start_col + 1 == end_col and self._turn == "WHITE":
                if landing_space != '00':
                    return True
            if start_col - 1 == end_col and self._turn == "BLACK":
                if landing_space != '00':
                    return True

        else:
            return False

    def validate_rook(self, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
        """validates whether the move is legal specifically for the rook.

        Args: start_row: An integer representing the starting row of the moving piece.
            start_col: An integer representing the starting column of the moving piece.
            end_row: An integer representing the starting row of the landing space.
            end_col: An integer representing the starting column of the landing space.

        Returns: A boolean value that signifies if the move is valid.
        """
        # Rules for column changing movement of the rook.
        if start_row == end_row:
            for i in range(start_col + 1, end_col):
                if self._board[start_row][i] != '00':
                    return False
            return True

        # Rules for row changing movement of the rook.
        elif start_col == end_col:
            for i in range(start_row + 1, end_row):
                if self._board[i][start_col] != '00':
                    return False
            return True

        else:
            return False

    def validate_knight(self, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
        """validates whether the move is legal specifically for the rook.

        Args: start_row: An integer representing the starting row of the moving piece.
            start_col: An integer representing the starting column of the moving piece.
            end_row: An integer representing the starting row of the landing space.
            end_col: An integer representing the starting column of the landing space.

        Returns: A boolean value that signifies if the move is valid.
        """
        # Rules for a knight moving one row and two columns.
        if abs(start_row - end_row) == 1:
            if abs(start_col - end_col) == 2:
                return True

        # Rules for a knight moving two rows and one column.
        elif abs(start_row - end_row) == 2:
            if abs(start_col - end_col) == 1:
                return True

        else:
            return False

    def validate_bishop(self, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
        """validates whether the move is legal specifically for the bishop.

        Args: start_row: An integer representing the starting row of the moving piece.
            start_col: An integer representing the starting column of the moving piece.
            end_row: An integer representing the starting row of the landing space.
            end_col: An integer representing the starting column of the landing space.

        Returns: A boolean value that signifies if the move is valid.
        """
        if abs(start_row - end_row) == abs(start_col - end_col):  # Ensures the bishop will move diagonally.
            dist = abs(start_row - end_row)
            if end_row > start_row and end_col > start_col:  # Increasing row and column
                for i in range(1, dist):
                    if self._board[start_row + i][start_col + i] != '00':
                        return False
            if end_row > start_row and end_col < start_col:  # Increasing row and decreasing column
                for i in range(1, dist):
                    if self._board[start_row + i][start_col - i] != '00':
                        return False
            if end_row < start_row and end_col > start_col:  # Decreasing row and increasing column
                for i in range(1, dist):
                    if self._board[start_row - i][start_col + i] != '00':
                        return False
            if end_row < start_row and end_col < start_col:  # Decreasing row and column
                for i in range(1, dist):
                    if self._board[start_row - i][start_col - i] != '00':
                        return False
            return True

        else:
            return False


    def validate_queen(self, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
        """validates whether the move is legal specifically for the queen.

        Args: start_row: An integer representing the starting row of the moving piece.
            start_col: An integer representing the starting column of the moving piece.
            end_row: An integer representing the starting row of the landing space.
            end_col: An integer representing the starting column of the landing space.

        Returns: A boolean value that signifies if the move is valid."""
        if abs(start_row - end_row) == abs(start_col - end_col):  # Rules for the queen moving diagonally.
            dist = abs(start_row - end_row)
            if end_row > start_row and end_col > start_col:  # Increasing row and column
                for i in range(1, dist):
                    if self._board[start_row + i][start_col + i] != '00':
                        return False
            if end_row > start_row and end_col < start_col:  # Increasing row and decreasing column
                for i in range(1, dist):
                    if self._board[start_row + i][start_col - i] != '00':
                        return False
            if end_row < start_row and end_col > start_col:  # Decreasing row and increasing column
                for i in range(1, dist):
                    if self._board[start_row - i][start_col + i] != '00':
                        return False
            if end_row < start_row and end_col < start_col:  # Decreasing row and column
                for i in range(1, dist):
                    if self._board[start_row - i][start_col - i] != '00':
                        return False
            return True

        # Rules for column only changing movement of the queen.
        elif start_row == end_row:
            for i in range(start_col + 1, end_col):
                if self._board[start_row][i] != '00':
                    return False
            return True

        # Rules for row only changing movement of the queen.
        elif start_col == end_col:
            for i in range(start_row + 1, end_row):
                if self._board[i][start_col] != '00':
                    return False
            return True

        else:
            return False



    def validate_king(self, start_row: int, start_col: int, landing_space: str, end_row: int, end_col: int) -> bool:
        """validates whether the move is legal specifically for the king.

        Args: start_row: An integer representing the starting row of the moving piece.
            start_col: An integer representing the starting column of the moving piece.
            landing_space: A string representing the value of the intended landing space of the moving piece.
            end_row: An integer representing the starting row of the landing space.
            end_col: An integer representing the starting column of the landing space.

        Returns: A boolean value that signifies if the move is valid.
        """
        # Rules for the King changing rows.
        if abs(start_row - end_row) == 1:
            if start_col == end_col or abs(start_col - end_col) == 1:
                if landing_space == '00':
                    return True

        # Rules for the King changing columns.
        elif abs(start_col - end_col) == 1:
            if start_row == end_row or abs(start_row - end_row) == 1:
                if landing_space == '00':
                    return True

        else:
            return False

    def atomic_landing(self, end_row: int, end_col: int):
        """This method is called when a chess piece legally lands on another, thereby capturing it and destroying all
        adjacent pieces except for pawns. The process is first run on a duplicate test board and then calls to
        check_king to ensure the move doesn't destroy both kings. If it doesn't, the real board is changed.

        Args: start_row: An integer representing the starting row of the moving piece.
            start_col: An integer representing the starting column of the moving piece.
            landing_space: A string representing the value of the intended landing space of the moving piece.
            end_row: An integer representing the starting row of the landing space.
            end_col: An integer representing the starting column of the landing space.

        Returns: True if the capture leaves 1 or more kings alive.
            False if the capture destroys both kings.
        """
        # The process is tested on a duplicate board first to ensure that at least one king survives the move.
        test_board = self._board
        test_board[end_row][end_col] = '00'  # Clear the landing space
        if end_col > 0 and "P" not in test_board[end_row][end_col - 1]:
            test_board[end_row][end_col - 1] = '00'  # Clear left of landing
        if end_col < 7 and "P" not in test_board[end_row][end_col + 1]:
            test_board[end_row][end_col + 1] = '00'  # Clear right of landing

        if end_row > 0 and "P" not in test_board[end_row - 1][end_col]:
            test_board[end_row - 1][end_col] = '00'  # Clear above landing
        if end_col > 0 and end_row > 0 and "P" not in test_board[end_row - 1][end_col - 1]:
            test_board[end_row - 1][end_col - 1] = '00'  # Clear upper left of landing
        if end_col < 7 and end_row > 0 and "P" not in test_board[end_row - 1][end_col + 1]:
            test_board[end_row - 1][end_col + 1] = '00'  # Clear upper right of landing

        if end_row < 7 and "P" not in test_board[end_row + 1][end_col]:
            test_board[end_row + 1][end_col] = '00'  # Clear below landing
        if end_col > 0 and end_row < 7 and "P" not in test_board[end_row + 1][end_col - 1]:
            test_board[end_row + 1][end_col - 1] = '00'  # Clear lower left of landing
        if end_col < 7 and end_row < 7 and "P" not in test_board[end_row + 1][end_col + 1]:
            test_board[end_row + 1][end_col + 1] = '00'  # Clear lower right of landing
        test_value = self.check_king(test_board)  # Check which kings are present.
        if test_value == False:
            return False  # If both kings are destroyed, then false.

        self._board[end_row][end_col] = '00'  # Clear the landing space
        if end_col > 0 and "P" not in self._board[end_row][end_col - 1]:
            self._board[end_row][end_col - 1] = '00'  # Clear left of landing
        if end_col < 7 and "P" not in self._board[end_row][end_col + 1]:
            self._board[end_row][end_col + 1] = '00'  # Clear right of landing

        if end_row > 0 and "P" not in self._board[end_row - 1][end_col]:
            self._board[end_row - 1][end_col] = '00'  # Clear above landing
        if end_col > 0 and end_row > 0 and "P" not in self._board[end_row - 1][end_col - 1]:
            self._board[end_row - 1][end_col - 1] = '00'  # Clear upper left of landing
        if end_col < 7 and end_row > 0 and "P" not in self._board[end_row - 1][end_col + 1]:
            self._board[end_row - 1][end_col + 1] = '00'    # Clear upper right of landing

        if end_row < 7 and "P" not in self._board[end_row + 1][end_col]:
            self._board[end_row + 1][end_col] = '00'  # Clear below landing
        if end_col > 0 and end_row < 7 and "P" not in self._board[end_row + 1][end_col - 1]:
            self._board[end_row + 1][end_col - 1] = '00'  # Clear lower left of landing
        if end_col < 7 and end_row < 7 and "P" not in self._board[end_row + 1][end_col + 1]:
            self._board[end_row + 1][end_col + 1] = '00'  # Clear lower right of landing
        self.check_king(self._board)
        return True

    def check_king(self, chessboard) -> bool:
        """This method is called whenever a piece is captured to determine if both kings are still on the board,
        both have been destroyed, or if one king is left. If one king is left, then the _game_state data member will be
        changed to reflect who has won.

        Args: chessboard: A list of lists that will either be a duplicate test board or the board actually being played.

        Returns: True if both or only one king is still on the board after the capture.
            False if both kings are destroyed by the capture.
        """
        black_present = False
        white_present = False
        for row in chessboard:  # Iterates through the board looking for each king.
            if "BK" in row:
                black_present = True
            if "WK" in row:
                white_present = True

        if not white_present and not black_present:  # Fail the atomic landing test if both kings are destroyed.
            return False

        if black_present and white_present:  # Return without changing the game state if both kings survive.
            return True

        # Change the game state if a single king has been destroyed.
        elif black_present:
            self._game_state = "BLACK_WON"
        else:
            self._game_state = "WHITE_WON"
        return True
