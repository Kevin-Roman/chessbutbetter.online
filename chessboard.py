# Stores all the information for each instance of a chess game
class Chessboard:
    def __init__(self):
        self.chessboard = [
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]]

    # Takes in two coordinates, moves the piece from the previous square to the new_square and then sets the previous square value to 0
    def move(self, previous_square, new_square):
        print(previous_square, new_square)

        piece = self.chessboard[previous_square[1]][previous_square[0]]
        self.chessboard[previous_square[1]][previous_square[0]] = 0
        self.chessboard[new_square[1]][new_square[0]] = piece

    # returns a string representation of the chessboard
    def __str__(self):
        str_chessboard = ""
        for x in range(8):
            str_chessboard += f"{x+1}  "

            for y in range(8):
                piece_in_square = str(self.chessboard[x][y])

                str_chessboard += f'{piece_in_square}{" "*(3-len(piece_in_square))}'

            str_chessboard += "\n"

        str_chessboard += "   a  b  c  d  e  f  g  h\n"

        return str_chessboard

    # converts notation format to coordinate format (e.g. from "a1" to (0,0))
    @staticmethod
    def notation_to_coord(notation):
        x, y = list(notation)

        x_axis = {"a": 0, "b": 1, "c": 2, "d": 3,
                  "e": 4, "f": 5, "g": 6, "h": 7}

        return (x_axis[x], int(y)-1)

    # converts notation format to coordinate format (e.g. from (0,0)  to "a1")
    @staticmethod
    def coord_to_notation(coord):
        x, y = list(coord)

        x_axis = {0: "a", 1: "b", 2: "c", 3: "d",
                  4: "e", 5: "f", 6: "g", 7: "h"}

        return (x_axis[x], y+1)


if __name__ == "__main__":

    chess = Chessboard()

    print(chess)

    chess.move((0, 0), (4, 3))
    print(chess)

    current_square = chess.notation_to_coord("f2")
    next_square = chess.notation_to_coord("d5")
    chess.move(current_square, next_square)
    print(chess)
