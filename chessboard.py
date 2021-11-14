class Chessboard:  # create the chessboard attribute to the class
    def __init__(self):
        self.chessboard = [
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]]
        # creates the chessboard, with black pieces at the bottom, and black on the top. E.g. wR means white Rook. 0 means empty sqaure. The rest of the squares are just temporary placeholder. I will add different pieces to the chessboard later.

    # returns a visual string representation of the chessboard when instance is asked for the string version.
    def __str__(self):
        str_chessboard = ""
        for x in range(8):
            for y in range(8):
                piece_in_square = str(self.chessboard[x][y])
                # retrieves the value in the specific square
                str_chessboard += f'{piece_in_square}{" "*(3-len(piece_in_square))}'
                # adds the value of the piece_in_square as well as a specific number of empty spaces following it (depending on how long the name of the piece is) so that every square has an equal padding around it
            str_chessboard += "\n"  # indicates new line for each row in the chessboard

        return str_chessboard

    # moves the piece from the current square to the next square, and sets the value of the current square to 0
    def move(self, current_square, next_square):
        print(current_square, next_square)
        # gets the element in the current square
        piece = self.chessboard[current_square[1]][current_square[0]]
        # sets the current square to the value of 0 (as the chess piece has moved from there so it is now empty.)
        self.chessboard[current_square[1]][current_square[0]] = 0
        # sets the next square element to piece variable (the piece that is being moved)
        self.chessboard[next_square[1]][next_square[0]] = piece

    @staticmethod  # built in decorator that defines a static method in the class in python
    def notation_to_coord(notation):
        # turns each character in the notation string to an element of a list
        x, y = list(notation)

        x_axis = {"a": 0, "b": 1, "c": 2, "d": 3,
                  "e": 4, "f": 5, "g": 6, "h": 7}

        return (x_axis[x], int(y)-1)

    @staticmethod
    def coord_to_notation(coord):
        x, y = list(coord)

        x_axis = {0: "a", 1: "b", 2: "c", 3: "d",
                  4: "e", 5: "f", 6: "g", 7: "h"}

        return (x_axis[x], int(y)+1)


if __name__ == "__main__":  # Only runs this code if this file is not imported
    # Creates an instance of the Chessboard class and store it in the chess variable
    chess = Chessboard()
    print(chess)

    chess.move((0, 1), (3, 0))  # move piece from index [0][1] with [3][0]
    print(chess)

    current_square = chess.notation_to_coord("f2")
    next_square = chess.notation_to_coord("d5")
    chess.move(current_square, next_square)
    print(chess)
