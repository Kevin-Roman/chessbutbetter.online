import jsonpickle

from chessboard import Chessboard


# Deserialises an instance of the Game class.
def deserialise(serialised_object):
    return jsonpickle.decode(serialised_object)


# Stores all the information for each instance of a chess game
# Can be considered as an offline multiplayer game
class Game:
    def __init__(self):
        self.chess = Chessboard()
        self._current_turn = 0
        self._winner = None
        self._checkmate = False
        self._draw = False

    def get_current_turn(self):
        return self._current_turn

    def change_current_turn(self):
        if self._current_turn == 0:
            self._current_turn = 1
        else:
            self._current_turn = 0

    def get_winner(self):
        return self._winner

    def set_winner(self, winner_id=None):
        self._winner = winner_id

    def get_is_checkmate(self):
        return self._checkmate

    def set_is_checkmate(self, checkmate=False):
        self._checkmate = checkmate

    def get_is_draw(self):
        return self._draw

    def set_is_draw(self, draw=False):
        self._draw = draw

    # Sets the winner, checkmate, and draw attributes if game has ended
    def end_game(self, winner_id, checkmate_or_draw):
        if checkmate_or_draw == 'checkmate':
            self.set_is_checkmate(True)

        elif checkmate_or_draw == 'draw':
            self.set_is_draw(True)

        self.set_winner(winner_id)

    # Executes the legal move, and returns all the new legal_moves
    def next_move(self, move, mutual_draw=False):
        coord1 = self.chess.notation_to_coord(move[:2])
        coord2 = self.chess.notation_to_coord(move[2:4])

        # The string variable 'move' could have a 5th character which represents the special move
        if len(move) == 4:
            special_move = None
        else:
            special_move = int(move[-1])

        # If the move is legal, make the move, and add it to the history of moves
        if coord2 in [legal_move[0] for legal_move in self.chess.get_all_legal_moves(coord1)]:
            # print(self.chess.get_all_legal_moves(
            #     coord1), coord2 + str(special_move))
            self.chess.move_and_special_moves(coord1, coord2, special_move)
            self.change_current_turn()
        else:
            return None

        # checks the opposing side if they have any legal_moves to make. If they don't then its end game.
        is_checkmate_or_draw = self.chess.is_checkmate_or_draw(
            self.get_current_turn())

        # print(self.get_current_turn(), str(is_checkmate_or_draw))

        if is_checkmate_or_draw:
            if self.get_current_turn() == 0:
                winner_colour = 1
            else:
                winner_colour = 0

            self.end_game(winner_colour, is_checkmate_or_draw)
            return None

        # If both players have agreed to draw, game is set to a draw
        if mutual_draw:
            self.end_game('draw', 'draw')
            return None

        return self.available_move_dictionary()

    # Returns a dictionary containing the from and to coordinates of all legal moves
    def available_move_dictionary(self):
        all_legal_moves = {}

        for num_row, row in enumerate(self.chess.chessboard):
            for num_column, _ in enumerate(row):
                coord = (num_column, num_row)
                square = self.chess.get_square(coord)
                if square != 0:

                    legal_moves_and_special_moves = self.chess.get_all_legal_moves(
                        coord)

                    legal_moves_and_special_moves = [
                        self.chess.coord_to_notation(lm) + str((sm or '')) for lm, sm in legal_moves_and_special_moves]

                    all_legal_moves[self.chess.coord_to_notation(
                        coord)] = legal_moves_and_special_moves

        return all_legal_moves

    def position_dictionary(self):
        positions = {}

        for num_row, row in enumerate(self.chess.chessboard):
            for num_column, _ in enumerate(row):
                coord = (num_column, num_row)
                square = self.chess.get_square(coord)

                if square != 0:
                    positions[self.chess.coord_to_notation(
                        coord)] = str(square)

        return positions

    # Serialises the instance of this class
    def serialise(self):
        return jsonpickle.encode(self)


if __name__ == "__main__":
    game = Game()
    print(game.chess)

    print(game.next_move("b1a3"))

    print(game.chess)

    game.end_game(1, 'checkmate')
    print(game.get_winner(), game.get_is_checkmate())
    game.end_game(2, 'draw')
    print(game.get_winner(), game.get_is_draw())

    print(game.position_dictionary())
