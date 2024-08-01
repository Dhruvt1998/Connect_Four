import math
import random
import time
import tracemalloc

class MinimaxPlayer:
    def __init__(self, player_number, depth=4):
        self.player_number = player_number
        self.depth = depth
        self.visited_nodes = 0

    def evaluate_window(self, window, player):
        score = 0
        opponent = 3 - player
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def score_position(self, board, player):
        score = 0
        rows, cols = board.shape
        # Center column
        center_array = [int(i) for i in list(board[:, cols // 2])]
        center_count = center_array.count(player)
        score += center_count * 3

        # Horizontal
        for row in range(rows):
            row_array = [int(i) for i in list(board[row, :])]
            for col in range(cols - 3):
                window = row_array[col:col + 4]
                score += self.evaluate_window(window, player)

        # Vertical
        for col in range(cols):
            col_array = [int(i) for i in list(board[:, col])]
            for row in range(rows - 3):
                window = col_array[row:row + 4]
                score += self.evaluate_window(window, player)

        # Positive diagonal
        for row in range(rows - 3):
            for col in range(cols - 3):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        # Negative diagonal
        for row in range(rows - 3):
            for col in range(cols - 3):
                window = [board[row + 3 - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score

    def is_terminal_node(self, game):
        return game.check_winner(self.player_number) or game.check_winner(3 - self.player_number) or len(game.get_valid_locations()) == 0

    def minimax(self, game, depth, maximizingPlayer):
        self.visited_nodes += 1
        valid_locations = game.get_valid_locations()
        is_terminal = self.is_terminal_node(game)
        if depth == 0 or is_terminal:
            if is_terminal:
                if game.check_winner(self.player_number):
                    return (None, 100000000000000)
                elif game.check_winner(3 - self.player_number):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(game.board, self.player_number))
        if maximizingPlayer:
            value = -math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = game.board.copy()
                game.drop_disc(col)
                new_score = self.minimax(game, depth-1, False)[1]
                game.board = b_copy
                if new_score > value:
                    value = new_score
                    best_col = col
            return best_col, value

        else:  # Minimizing player
            value = math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = game.board.copy()
                game.drop_disc(col)
                new_score = self.minimax(game, depth-1, True)[1]
                game.board = b_copy
                if new_score < value:
                    value = new_score
                    best_col = col
            return best_col, value

    def choose_move(self, game):
        self.visited_nodes = 0
        tracemalloc.start()
        start_time = time.time()
        col, minimax_score = self.minimax(game, self.depth, True)
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        duration = end_time - start_time
        return col, duration, peak / 1024, self.visited_nodes  # Memory in KB
