import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from connect_four import ConnectFour
from minimax_player import MinimaxPlayer
from minimax_alpha_beta_player import MinimaxAlphaBetaPlayer
from mcts_player import MCTSPlayer

def play_game_with_algorithm(game, algorithm1, fixed_algorithm, player1_number, player2_number):
    performance_stats = {
        "move": [],
        "time": [],
        "memory": [],
        "visited_nodes": [],
        "winner": None
    }

    game.reset_game()
    turn = 0
    move_number = 0

    while not game.check_winner(player1_number) and not game.check_winner(player2_number) and game.get_valid_locations():
        if turn % 2 == 0:
            col, duration, memory, visited_nodes = algorithm1.choose_move(game)
            performance_stats["move"].append(move_number)
            performance_stats["time"].append(duration)
            performance_stats["memory"].append(memory)
            performance_stats["visited_nodes"].append(visited_nodes)
            move_number += 1
        else:
            col, _, _, _ = fixed_algorithm.choose_move(game)

        if game.is_valid_location(col):
            game.drop_disc(col)
            game.print_board()  # Print the board after each move
            if game.check_winner(player1_number):
                performance_stats["winner"] = "Player 1"
                break
            elif game.check_winner(player2_number):
                performance_stats["winner"] = "Player 2"
                break
            game.switch_player()
        turn += 1

    if performance_stats["winner"] is None:
        performance_stats["winner"] = "Draw"

    return performance_stats

def compare_algorithms():
    game = ConnectFour()

    minimax_player = MinimaxPlayer(1, depth=4)
    alpha_beta_player = MinimaxAlphaBetaPlayer(1, depth=4)
    mcts_player = MCTSPlayer(1, simulations=1000)
    fixed_algorithm = MinimaxAlphaBetaPlayer(2, depth=4)  # Fixed algorithm for Player 2

    print("Comparing Minimax vs Fixed Algorithm (Alpha-Beta)")
    stats_minimax = play_game_with_algorithm(game, minimax_player, fixed_algorithm, 1, 2)

    print("Comparing Alpha-Beta vs Fixed Algorithm (Alpha-Beta)")
    stats_alpha_beta = play_game_with_algorithm(game, alpha_beta_player, fixed_algorithm, 1, 2)

    print("Comparing MCTS vs Fixed Algorithm (Alpha-Beta)")
    stats_mcts = play_game_with_algorithm(game, mcts_player, fixed_algorithm, 1, 2)

    plot_performance(stats_minimax, stats_alpha_beta, stats_mcts)
    print_performance_table(stats_minimax, stats_alpha_beta, stats_mcts)

def plot_performance(stats_minimax, stats_alpha_beta, stats_mcts):
    plt.figure(figsize=(12, 6))
    plt.title('Time Comparison (Player 1)')
    plt.xlabel('Move')
    plt.ylabel('Time (s)')
    plt.plot(stats_minimax["move"], stats_minimax["time"], label='Minimax')
    plt.plot(stats_alpha_beta["move"], stats_alpha_beta["time"], label='Alpha-Beta')
    plt.plot(stats_mcts["move"], stats_mcts["time"], label='MCTS')
    plt.legend()
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.title('Memory Usage Comparison (Player 1)')
    plt.xlabel('Move')
    plt.ylabel('Memory (KB)')
    plt.plot(stats_minimax["move"], stats_minimax["memory"], label='Minimax')
    plt.plot(stats_alpha_beta["move"], stats_alpha_beta["memory"], label='Alpha-Beta')
    plt.plot(stats_mcts["move"], stats_mcts["memory"], label='MCTS')
    plt.legend()
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.title('Visited Nodes Comparison (Player 1)')
    plt.xlabel('Move')
    plt.ylabel('Visited Nodes')
    plt.plot(stats_minimax["move"], stats_minimax["visited_nodes"], label='Minimax')
    plt.plot(stats_alpha_beta["move"], stats_alpha_beta["visited_nodes"], label='Alpha-Beta')
    plt.plot(stats_mcts["move"], stats_mcts["visited_nodes"], label='MCTS')
    plt.legend()
    plt.show()

def print_performance_table(stats_minimax, stats_alpha_beta, stats_mcts):
    df_minimax = pd.DataFrame(stats_minimax)
    df_alpha_beta = pd.DataFrame(stats_alpha_beta)
    df_mcts = pd.DataFrame(stats_mcts)

    print("\nMinimax Performance:")
    print(df_minimax)

    print("\nAlpha-Beta Pruning Performance:")
    print(df_alpha_beta)

    print("\nMCTS Performance:")
    print(df_mcts)

    print(f"\nWinner of Minimax: {stats_minimax['winner']}")
    print(f"Winner of Alpha-Beta Pruning: {stats_alpha_beta['winner']}")
    print(f"Winner of MCTS: {stats_mcts['winner']}")

compare_algorithms()
