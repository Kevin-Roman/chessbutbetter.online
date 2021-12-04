# Piece superclass and all the different pieces subclasses

# Class for the piece type
class Piece:
    def __init__(self):
        self._straight = False
        self._diagonal = False

        self._already_moved = False
        self._available_moves = []

        self._name = " "
        self._colour = 0  # 0 = white, 1 = black
        self._value = 0

    def get_straight(self):
        return self._straight

    def set_straight(self, straight):
        self._straight = straight

    def get_diagonal(self):
        return self._diagonal

    def set_diagonal(self, diagonal):
        self._diagonal = diagonal

    def get_available_moves(self):
        return self._available_moves

    def set_available_moves(self, available_moves):
        self._available_moves = available_moves

    def get_all_moves(self):
        return [self._straight, self._diagonal, self._available_moves]

    def get_already_moved(self):
        return self._already_moved

    def set_already_moved(self, already_moved):
        self._already_moved = already_moved

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_colour(self):
        return self._colour

    def set_colour(self, colour):
        self._colour = colour

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def __str__(self):
        if self.get_colour() == 1:
            colour = "black"
        else:
            colour = "white"

        name = self.get_name()
        if name == "Knight":
            name = "N"

        return f"{colour[0]}{name[0]}"


# Pawn subclass which inherits all the members of the Piece class.
class Pawn(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("Pawn")
        self.set_colour(colour)
        self.set_value(1)

        moves = [[-1, 2, -1],
                 [3, 1, 3],
                 [-1, 0, -1]]

        if colour == 1:
            self.set_available_moves(moves)
        else:
            self.set_available_moves(moves[::-1])


# Knight subclass which inherits all the members of the Piece class.
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


# Bishop subclass which inherits all the members of the Piece class.
class Bishop(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("Bishop")
        self.set_colour(colour)
        self.set_value(3)
        self.set_diagonal(True)


# Rook subclass which inherits all the members of the Piece class.
class Rook(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("Rook")
        self.set_colour(colour)
        self.set_value(5)
        self.set_straight(True)


# Queen subclass which inherits all the members of the Piece class.
class Queen(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("Queen")
        self.set_colour(colour)
        self.set_value(9)
        self.set_straight(True)
        self.set_diagonal(True)


# King subclass which inherits all the members of the Piece class.
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
