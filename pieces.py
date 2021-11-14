class Piece:
    def __init__(self):
        # indicates whether the piece is able to move straight in any direction
        self.straight = False
        # indicates whether the piece is able to move diagonally in any direction
        self.diagonal = False

        self.already_moved_once = False
        self.available_moves = []

        self.name = " "
        self.colour = 0
        self.value = 0

    def get_straight(self):
        return self.straight

    def set_straight(self, straight):
        self.straight = straight

    def get_diagonal(self):
        return self.diagonal

    def set_diagonal(self, diagonal):
        self.diagonal = diagonal

    def get_available_moves(self):
        return self.available_moves

    def set_available_moves(self, available_moves=[]):
        self.available_moves = available_moves

    def get_all_moves(self):
        return [self.straight, self.diagonal, self.available_moves]

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_colour(self):
        return self.colour

    def set_colour(self, colour):
        self.colour = colour

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def __str__(self):
        if self.get_colour() == 1:
            colour = "black"
        else:
            colour = "white"

        name = self.get_name()
        if name == "Knight":
            name = "N"  # As King also starts with the letter K, N is the convention for the knight

        # returns a string representation of the chess piece
        return f"{colour[0]}{name[0]}"


# Create a Pawn subclass which inherits the Piece class.
class Pawn(Piece):
    def __init__(self, colour):
        super().__init__()  # inherits all the attributes from from the Piece class without needing to explicitly refer to the Superclass

        self.set_name("Pawn")
        self.set_colour(colour)
        self.set_value(1)

        # sets all the moves that the pawn can make in relation to its position. 0 is the pawn's current position. -1 being are squares the piece cannot move to. 1, 2, 3 are all moves that a Pawn could potentially make, but more data is needed to determine whether the move is currently possible.
        moves = [[-1, 2, -1],
                 [3, 1, 3],
                 [-1, 0, -1]]

        if colour == 1:
            self.set_available_moves(moves)
        else:
            # reverses the order of the lists inside the moves list
            self.set_available_moves(moves[::-1])


class Knight(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("Knight")
        self.set_colour(colour)
        self.set_value(3)

        self.set_available_moves([[-1, 1, -1, 1, -1],
                                  [1, -1, -1, -1, 1],
                                  [-1, -1, 0, -1, -1],
                                  [1, -1, -1, -1, 1],
                                  [-1, 1, -1, 1, -1]])


class Bishop(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("Bishop")
        self.set_colour(colour)
        self.set_value(3)
        self.set_diagonal(True)


class Rook(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("Rook")
        self.set_colour(colour)
        self.set_value(5)
        self.set_straight(True)


class Queen(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("Queen")
        self.set_colour(colour)
        self.set_value(9)
        self.set_straight(True)
        self.set_diagonal(True)


class King(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("King")
        self.set_colour(colour)
        self.set_value(100)

        # A king move to a square with a 4 is only possible due to castling
        self.set_available_moves([[-1, 1, 1, 1, -1],
                                  [4, 1, 0, 1, 4],
                                  [-1, 1, 1, 1, -1]])


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
        print(
            piece.get_name(), piece.get_colour(), piece.get_value(), piece.get_all_moves(), piece, "\n")
