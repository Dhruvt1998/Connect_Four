import numpy as np


class ConnectFour:
    ROWS = 6
    COLS = 7

    def __init__(self):
        self.board = np.zeros((self.ROWS, self.COLS))
        self.current_player = 1

    def drop_disc(self, col):
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                break

    def is_valid_location(self, col):
        return self.board[0][col] == 0

    def get_valid_locations(self):
        return [col for col in range(self.COLS) if self.is_valid_location(col)]

    def check_winner(self, player):
        # Check horizontal locations
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if all(self.board[row, col + i] == player for i in range(4)):
                    return True

        # Check vertical locations
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if all(self.board[row + i, col] == player for i in range(4)):
                    return True

        # Check positively sloped diagonals
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if all(self.board[row + i, col + i] == player for i in range(4)):
                    return True

        # Check negatively sloped diagonals
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                if all(self.board[row - i, col + i] == player for i in range(4)):
                    return True

        return False

    def print_board(self):
        print(np.flip(self.board, 0))

    def reset_game(self):
        self.board = np.zeros((self.ROWS, self.COLS))
        self.current_player = 1

    def switch_player(self):
        self.current_player = 3 - self.current_player  # Switches between 1 and 2
