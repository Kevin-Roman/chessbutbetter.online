from chessboard import Chessboard


class Game:
    """Stores all the information for each instance of a chess game
    Can be considered as an offline multiplayer game
    """

    def __init__(self):
        self.chess = Chessboard()
        # colour of the current turn (0 = white, 1 = black)
        self.current_turn = 0
        self.winner = None  # colour of winner or "draw"
        self.is_checkmate = False
        self.is_draw = False

    def change_current_turn(self):
        if self.current_turn == 0:
            self.current_turn = 1
        else:
            self.current_turn = 0

    def end_game(self, winner_colour, checkmate_or_draw):
        """Sets the winner's colour, checkmate, and draw attributes if game has ended

        Args:
            winner_colour (int/str): integer colour of the winner or "draw"
            checkmate_or_draw (str): either "checkmate" or "draw"
        """

        if checkmate_or_draw == 'checkmate':
            self.is_checkmate = True

        elif checkmate_or_draw == 'draw':
            self.is_draw = True

        self.winner = winner_colour

    def next_move(self, move, mutual_draw=None):
        """Executes the legal move, and returns all the new legal_moves

        Args:
            move (str): the move in algebraic notation form where the starting square, ending square, and special move number are joined together. e.g. "a2a32", a2 = start_coord, a3 = end_coord, 2 = special move type.
            mutual_draw (bool, optional): Defaults to None.

        Returns:
            NoneType/dict: None if move is not legal or dictionary of all the available moves of every piece after the move was executed if move is legal
        """

        if mutual_draw is None:
            mutual_draw = False

        start_coord = self.chess.notation_to_coord(move[:2])
        end_coord = self.chess.notation_to_coord(move[2:4])

        # The string variable 'move' could have a 5th character which represents the special move.
        # If its only 4 characters long then special move type is equal to None
        if len(move) == 4:
            special_move = None
        else:
            special_move = int(move[-1])

        # If the move is legal, make the move, and add it to the history of moves
        if end_coord in [legal_move[0] for legal_move in self.chess.get_legal_moves(start_coord)]:
            self.chess.move_and_special_moves(
                start_coord, end_coord, special_move)
            # once move is executed, change the turn
            self.change_current_turn()
        else:
            return None

        # checks the opposing side if they have any legal_moves to make. If they don't then its end game.
        is_checkmate_or_draw = self.chess.is_checkmate_or_draw(
            self.current_turn)

        # print(self.current_turn, str(is_checkmate_or_draw))

        if is_checkmate_or_draw:
            # If it is checkmate or draw, the winner is the opponent
            if self.current_turn == 0:
                winner_colour = 1
            else:
                winner_colour = 0

            self.end_game(winner_colour, is_checkmate_or_draw)
            return None

        # If both players have agreed to draw, game is set to a draw
        if mutual_draw:
            self.end_game('draw', 'draw')
            return None

        return self.available_moves_dictionary()

    def available_moves_dictionary(self):
        """Returns a dictionary containing the start and end coordinates of all legal moves

        Returns:
            dict: dictionary containing the from and to coordinates of all legal moves
        """

        all_legal_moves = {}  # {"a1": [], "a2": ["a31", "a42"], ...}

        for num_row, row in enumerate(self.chess.chessboard):
            for num_column, _ in enumerate(row):
                coord = (num_column, num_row)
                square = self.chess.get_square(coord)

                # if square is not empty
                if square != 0:

                    legal_moves = self.chess.get_legal_moves(
                        coord)

                    # converts each legal move to string format and adds the special move type number to the end of the string
                    legal_moves_string = [
                        self.chess.coord_to_notation(coord) + str((special_move or '')) for coord, special_move in legal_moves
                    ]

                    all_legal_moves[self.chess.coord_to_notation(
                        coord)] = legal_moves_string

        return all_legal_moves

    def position_dictionary(self):
        """Generates a dictionary the algebraic coordinate of where each piece is

        Returns:
            dict: dictionary where the keys are the algebriac coorindates and the values are the corresponding piece name and colours initials on that square
        """

        positions = {}

        for num_row, row in enumerate(self.chess.chessboard):
            for num_column, _ in enumerate(row):
                coord = (num_column, num_row)
                square = self.chess.get_square(coord)

                if square != 0:
                    positions[self.chess.coord_to_notation(
                        coord)] = str(square)

        return positions


class Game_AI(Game):
    def __init__(self, depth):
        # initialises the attributes of the superclass
        super().__init__()

        self.depth = depth


if __name__ == "__main__":
    game = Game()
    print(game.chess)

    # executes the move and then prints out the availables moves
    print(game.next_move("b1a3"))

    print(game.chess)

    game.end_game(1, 'checkmate')
    print(game.winner, game.is_checkmate)
    game.end_game(2, 'draw')
    print(game.winner, game.is_draw)
