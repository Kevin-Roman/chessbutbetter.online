import math
import random

# Piece type to piece value conversion
eval_position = {"P": 1, "B": 3, "N": 3, "R": 5, "Q": 9, "K": 1000}


# Receives a piece and returns its respective value depending on type and colour
def piece_value(piece, player_colour):
    value = eval_position[piece.get_name()[0]]

    # If the colour of the piece is the same as the player's colour then the value value is turned negative
    if piece.get_colour() == player_colour:
        value *= -1

    return value


# Calculates the total evaluation of the chessboard where a larger evaluation is better for the AI
def evaluate(chessboard, player_colour):
    total_eval_value = 0

    # Iterates through each square
    for num_row in range(8):
        for num_column in range(8):
            coord = (num_column, num_row)
            square = chessboard.get_square(coord)

            # If square contains a piece
            if square != 0:
                # Add the value of the piece to total_eval_value
                total_eval_value += piece_value(square, player_colour)

    return total_eval_value


# Uses the minimax algorithm to decide the best move the computer should make given the depth value given (how many moves ahead the algorithm will look at).
def minimax(chessboard, depth, player_colour):
    return maximise(chessboard, depth, -math.inf, math.inf, player_colour, True)


# Maximises the chessboard evaluation
def maximise(chessboard, depth, alpha, beta, player_colour, best_move_wanted):
    if depth == 0:
        return evaluate(chessboard, player_colour)

    # Sets max_eval to negative infinity
    max_eval = -math.inf
    best_move = []

    # Iterates through each square in the chessboard
    for num_row in range(8):
        for num_column in range(8):
            coord = (num_column, num_row)
            square = chessboard.get_square(coord)

            if square != 0 and square.get_colour() != player_colour:
                all_moves = chessboard.get_all_legal_moves(coord)

                # Get the best possible move the computer could make
                for move in all_moves:

                    chessboard.move_and_special_moves(coord, move[0], move[1])

                    score = minimise(chessboard, depth - 1,
                                     alpha, beta, player_colour)
                    # print(score)
                    chessboard.undo_move()

                    if best_move_wanted:
                        # Once the evaluation of each move is calculated, if the current move's evaluation score is greater than max_eval, set max_value to the current move's score.
                        if score > max_eval:
                            best_move = [(coord, move)]

                        elif score == max_eval:
                            # If multiple moves with the same best evalution, then append to the best_move list.
                            best_move.append((coord, move))

                    if score > max_eval:
                        max_eval = score

                    if max_eval > alpha:
                        alpha = max_eval

                    if alpha >= beta:
                        break

    if best_move_wanted:
        print(f"score: {max_eval}")
        # return the best move
        return best_move

    return max_eval


# Minimises the chessboard evaluation
def minimise(chessboard, depth, alpha, beta, player_colour):
    if depth == 0:
        return evaluate(chessboard, player_colour)

    # Sets max_eval to positive infinity
    min_eval = math.inf

    # Iterates through each square in the chessboard
    for num_row in range(8):
        for num_column in range(8):
            coord = (num_column, num_row)
            square = chessboard.get_square(coord)

            if square != 0 and square.get_colour() == player_colour:
                all_moves = chessboard.get_all_legal_moves(coord)

                # Get the best possible move the player could make
                for move in all_moves:

                    chessboard.move_and_special_moves(coord, move[0], move[1])

                    score = maximise(chessboard, depth - 1, alpha, beta,
                                     player_colour, False)

                    chessboard.undo_move()

                    if score < min_eval:
                        min_eval = score

                    if min_eval < beta:
                        beta = min_eval

                    if alpha >= beta:
                        break

    return min_eval


if __name__ == "__main__":
    import time

    # 0: play game, 1: time elapsed, 2: time elapsed with profile stats
    play_game = int(input("0, 1 or 2: "))

    from chessboard import Chessboard

    chess = Chessboard()

    def play(play_game=2):
        print(chess)

        # e.g. c2 = source square, 3c = target square, 2 = special move
        player_move = input('Your move (e.g. "c2c42"): ')
        source = chess.notation_to_coord(player_move[:2])
        target = chess.notation_to_coord(player_move[2:4])

        # if no special move specified, set special_move to None
        if len(player_move) > 4:
            special_move = int(player_move[-1])
        else:
            special_move = None

        piece = chess.get_square(source)

        print(chess.get_all_legal_moves(source))

        # validation to see if the move is legal for the user to make.
        if (target, special_move) in chess.get_all_legal_moves(source) and piece != 0 and piece.get_colour() == 0:
            # make the player's move
            chess.move_and_special_moves(source, target, special_move)

            if play_game == 0:
                # Set the depth value
                depth = 3

                # Gets the best move the computer could make, if there are several best moves, then random.choice will pick one at random.
                ai_move = random.choice(minimax(chess, depth, 0))

                ai_source = ai_move[0]
                ai_target, ai_special_move = ai_move[1]

                # make that move
                chess.move_and_special_moves(
                    ai_source, ai_target, ai_special_move)

            else:
                time_before = time.time()
                ai_move = random.choice(minimax(chess, 1, 0))
                print(f"Depth 1: {time.time() - time_before}")

                time_before = time.time()
                ai_move = random.choice(minimax(chess, 2, 0))
                print(f"Depth 2: {time.time() - time_before}")

                time_before = time.time()
                ai_move = random.choice(minimax(chess, 3, 0))
                print(f"Depth 3: {time.time() - time_before}")

        else:
            print("Not a legal move, try again.")

    if play_game == 0:
        # Play game whilst True
        while True:
            play(play_game)

    elif play_game == 1:
        play(play_game)

    else:
        import cProfile
        import pstats
        from pstats import SortKey

        # Creates instance of Profile class
        profile = cProfile.Profile()

        profile.runcall(play)
        ps = pstats.Stats(profile)
        # Displays the elasped time of functions in order of totaltime column
        ps.strip_dirs().sort_stats(SortKey.TIME).print_stats()
