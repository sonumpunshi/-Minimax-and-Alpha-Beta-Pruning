import sys
import argparse


def eval_function(game_state, is_maximizing_player):
    # get the number of red and blue marbles from the game state
    red_marbles = game_state['red']
    blue_marbles = game_state['blue']
    
    # if one player has no marbles left, the game is over
    if red_marbles == 0 or blue_marbles == 0:
        # if the maximizing player has no marbles left, return the lowest possible score
        if is_maximizing_player:
            score = float('inf')
        # if the minimizing player has no marbles left, return the highest possible score
        else:
            score = float('-inf')
    else:
        # calculate the score based on the difference between the number of red and blue marbles
        # a positive difference favors the maximizing player, while a negative difference favors the minimizing player
        score = (red_marbles * 2 - blue_marbles * 3) * (1 if is_maximizing_player else -1)

    # return the calculated score
    return score


def minmax_with_alpha_beta_pruning(game_state, depth, is_maximizing_player, alpha, beta):
    # if depth is not specified, set it to 3
    if depth is None:
        depth = 3

    # if the maximum depth is reached or the game is over, return the score of the current state
    if depth == 0 or is_game_over(game_state):
        return None, eval_function(game_state, is_maximizing_player)

    # initialize the best move and the available moves
    best_move = None
    moves = ['red', 'blue']

    if is_maximizing_player:
        # if it's the maximizing player's turn, initialize the maximum value to the lowest possible value
        max_value = float('-inf')
        # iterate over the available moves
        for move in moves:
            # if the current move is valid, create a new game state by subtracting one marble of the corresponding color
            if game_state[move] > 0:
                new_game_state = game_state.copy()
                new_game_state[move] -= 1
                # recursively call the minmax function with the new game state and
                # decreased depth, and switch the player
                _, value = minmax_with_alpha_beta_pruning(new_game_state, depth - 1, False, alpha, beta)
                # if the new value is greater than the current maximum value, update the maximum value and best move
                if value > max_value:
                    max_value = value
                    best_move = move
                # update alpha with the maximum value
                alpha = max(alpha, value)
                # if beta is less than or equal to alpha, pruning occurs, and the loop is broken
                if beta <= alpha:
                    break
        # return the best move and maximum value
        return best_move, max_value
    else:
        # if it's the minimizing player's turn, initialize the minimum value to the highest possible value
        min_value = float('inf')
        # iterate over the available moves
        for move in moves:
            # if the current move is valid, create a new game state by subtracting one marble of the corresponding color
            if game_state[move] > 0:
                new_game_state = game_state.copy()
                new_game_state[move] -= 1
                # recursively call the minmax function with the new game
                # state and decreased depth, and switch the player
                _, value = minmax_with_alpha_beta_pruning(new_game_state, depth - 1, True, alpha, beta)
                # if the new value is less than the current minimum value, update the minimum value and best move
                if value < min_value:
                    min_value = value
                    best_move = move
                # update beta with the minimum value
                beta = min(beta, value)
                # if beta is less than or equal to alpha, pruning occurs, and the loop is broken
                if beta <= alpha:
                    break
        # return the best move and minimum value
        return best_move, min_value


# This function calculates the winner and score of the game based on the current game state and the current player
def calculate_winner_and_score(game_state, current_player):
    # calculate the score based on the number of remaining marbles
    score = game_state['red'] * 2 + game_state['blue'] * 3
    # determine the winner based on the current player
    winner = "computer" if current_player == "human" else "human"
    # return the winner and score
    return winner, score


# This function checks if the game is over based on the current game state
def is_game_over(game_state):
    # if either the red or blue pile is empty, the game is over
    return game_state['red'] == 0 or game_state['blue'] == 0


# This function represents the computer's turn
def computer_turn(game_state, depth):
    # use the minmax algorithm with alpha-beta pruning to determine the best move
    best_move, _ = minmax_with_alpha_beta_pruning(game_state, depth, True, float('-inf'), float('inf'))
    # if a valid move is found, update the game state and print the computer's choice
    if best_move is not None:
        game_state[best_move] -= 1
        print(f"Computer chose {best_move} pile")
    # if no valid move is found, print a message
    else:
        print("No valid moves for the computer")


# This function represents the human's turn
def human_turn(game_state):
    # loop until a valid move is chosen
    while True:
        # ask the user to choose a pile to remove a marble from
        chosen_pile = input("Choose a pile to remove a marble from (red/blue): ").lower()
        # if the chosen pile is valid and has at least one marble left, update the game state and break out of the loop
        if chosen_pile in ["red", "blue"]:
            if game_state[chosen_pile] > 0:
                game_state[chosen_pile] -= 1
                break
            # if the chosen pile is empty, print a message and ask the user to choose another pile
            else:
                print(f"The {chosen_pile} pile is empty. Choose another pile.")
        # if the chosen pile is invalid, print a message and ask the user to choose again
        else:
            print("Invalid input. Choose either 'red' or 'blue' pile.")


# This function displays the current game state
def display_game_state(game_state):
    print(f"\nCurrent game state: Red marbles: {game_state['red']}, Blue marbles: {game_state['blue']}")


# This function parses the command-line arguments and returns the relevant values
def parse_arguments(args):
    parser = argparse.ArgumentParser(description="Red-Blue Nim Game")
    # add command-line arguments for the number of red and blue marbles, the first player, and the depth limit
    parser.add_argument("num_red", type=int, help="Number of red marbles")
    parser.add_argument("num_blue", type=int, help="Number of blue marbles")
    parser.add_argument("first_player", choices=["computer", "human"], default="computer", nargs="?",
                        help="Who starts the game: computer or human (default: computer)")
    parser.add_argument("depth", type=int, default=None, nargs="?",
                        help="Depth limit for depth-limited search (optional)")

    # parse the arguments and return the relevant values
    args = parser.parse_args(args[1:])
    return args.num_red, args.num_blue, args.first_player, args.depth


def main():
    # parse the command-line arguments to get the initial game state and first player
    num_red, num_blue, first_player, depth = parse_arguments(sys.argv)
    # initialize the game state and current player
    game_state = {"red": num_red, "blue": num_blue}
    current_player = first_player

    # loop until the game is over
    while not is_game_over(game_state):
        # display the current game state
        display_game_state(game_state)
        # if it's the human's turn, let them make a move
        if current_player == "human":
            human_turn(game_state)
        # if it's the computer's turn, use the minmax algorithm to make a move
        else:
            computer_turn(game_state, depth)
        # switch the current player
        current_player = "computer" if current_player == "human" else "human"

    # calculate the winner and score and print the result
    
    winner, score = calculate_winner_and_score(game_state, current_player)
    if winner=='human':
        winner='computer'
    else:
        winner='human'
    print(f"{winner.capitalize()} wins with a score of {score}!")


if __name__ == "__main__":
    main()
