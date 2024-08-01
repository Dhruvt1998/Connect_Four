import random
import time
import tracemalloc
import numpy as np

from connect_four import ConnectFour


class MCTSPlayer:
    def __init__(self, player_number, simulations=1000):
        self.player_number = player_number
        self.simulations = simulations
        self.visited_nodes = 0

    def choose_move(self, game):
        self.visited_nodes = 0
        tracemalloc.start()
        start_time = time.time()
        col = self.mcts(game)
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        duration = end_time - start_time
        return col, duration, peak / 1024, self.visited_nodes  # Memory in KB

    def mcts(self, game):
        valid_locations = game.get_valid_locations()
        best_move = random.choice(valid_locations)
        best_score = -float('inf')

        for col in valid_locations:
            self.visited_nodes += 1
            temp_game = ConnectFour()
            temp_game.board = np.copy(game.board)
            temp_game.current_player = self.player_number
            temp_game.drop_disc(col)
            score = self.simulate(temp_game)
            if score > best_score:
                best_score = score
                best_move = col

        return best_move

    def simulate(self, game):
        current_player = self.player_number
        for _ in range(self.simulations):
            temp_game = ConnectFour()
            temp_game.board = np.copy(game.board)
            temp_game.current_player = current_player
            while True:
                valid_locations = temp_game.get_valid_locations()
                if len(valid_locations) == 0:
                    break
                move = random.choice(valid_locations)
                temp_game.drop_disc(move)
                if temp_game.check_winner(temp_game.current_player):
                    return 1 if temp_game.current_player == self.player_number else -1
                temp_game.switch_player()
        return 0
