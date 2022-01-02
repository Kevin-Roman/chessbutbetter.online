# Piece superclass and all the different pieces subclasses

# Class for the piece type
class Piece:
    def __init__(self):
        self.straight = False
        self.diagonal = False

        self.already_moved = False
        self.available_moves = []

        self.name = " "
        self.colour = 0  # 0 = white, 1 = black
        self.value = 0

    def get_all_moves(self):
        return [self.straight, self.diagonal, self.available_moves]

    def __str__(self):
        if self.colour == 1:
            colour = "black"
        else:
            colour = "white"

        name = self.name
        if name == "Knight":
            name = "N"

        return f"{colour[0]}{name[0]}"


# Pawn subclass which inherits all the members of the Piece class.
class Pawn(Piece):
    def __init__(self, colour):
        super().__init__()

        self.name = "Pawn"
        self.colour = colour
        self.value = 1

        moves = [[-1, 2, -1],
                 [3, 1, 3],
                 [-1, 0, -1]]

        if colour == 1:
            self.available_moves = moves[::-1]
        else:
            self.available_moves = moves


# Knight subclass which inherits all the members of the Piece class.
class Knight(Piece):
    def __init__(self, colour):
        super().__init__()

        self.name = "Knight"
        self.colour = colour
        self.value = 3

        self.available_moves = [[-1, 1, -1, 1, -1],
                                [1, -1, -1, -1, 1],
                                [-1, -1, 0, -1, -1],
                                [1, -1, -1, -1, 1],
                                [-1, 1, -1, 1, -1]]


# Bishop subclass which inherits all the members of the Piece class.
class Bishop(Piece):
    def __init__(self, colour):
        super().__init__()

        self.name = "Bishop"
        self.colour = colour
        self.value = 3
        self.diagonal = True


# Rook subclass which inherits all the members of the Piece class.
class Rook(Piece):
    def __init__(self, colour):
        super().__init__()

        self.name = "Rook"
        self.colour = colour
        self.value = 5
        self.straight = True


# Queen subclass which inherits all the members of the Piece class.
class Queen(Piece):
    def __init__(self, colour):
        super().__init__()

        self.name = "Queen"
        self.colour = colour
        self.value = 9
        self.straight = True
        self.diagonal = True


# King subclass which inherits all the members of the Piece class.
class King(Piece):
    def __init__(self, colour):
        super().__init__()

        self.name = "King"
        self.colour = colour
        self.value = 100

        # A king move to a square with a 4 is only possible due to castling
        self.available_moves = [[-1, 1, 1, 1, -1],
                                [4, 1, 0, 1, 4],
                                [-1, 1, 1, 1, -1]]


if __name__ == "__main__":
    white_pawn = Pawn(0)
    white_bishop = Bishop(0)
    white_knight = Knight(0)
    white_rook = Rook(0)
    white_queen = Queen(0)
    white_king = King(0)

    black_pawn = Pawn(1)
    black_bishop = Bishop(1)
    black_knight = Knight(1)
    black_rook = Rook(1)
    black_queen = Queen(1)
    black_king = King(1)

    all_pieces = [
        white_pawn, white_bishop, white_knight, white_rook, white_queen,
        white_king, black_pawn, black_bishop, black_knight, black_rook, black_queen, black_king]

    for piece in all_pieces:
        print(piece.name, piece.colour, piece.value,
              piece.all_moves, piece, "\n")
