class Piece:
    def __init__(self):
        self.straight = False
        self.diagonal = False

        self.available_moves = []

        self.name = " "
        self.colour = 0
        self.value = 0

    def get_available_moves(self):
        return self.available_moves

    def set_available_moves(self, available_moves):
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


# Create a Pawn subclass which inherits the methods from the Piece class.
class Pawn(Piece):
    def __init__(self, colour):
        super().__init__()  # inherits all the attributes from from the Piece class without needing to explicitly refer to the Superclass

        self.set_name("Pawn")
        self.set_colour(colour)
        self.set_value(1)
        self.already_moved_once = False

        # sets all the moves that the pawn can make in relation to its position. 0 is the pawn's current position. -1 being are squares the piece cannot move to. 1, 2, 3 are all moves that a Pawn could potentially make, but more data is needed to determine whether the move is currently possible.
        self.set_available_moves([[-1, 2, -1],
                                  [3, 1, 3],
                                  [-1, 0, -1]])


class Knight(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("Knight")
        self.set_colour(colour)
        self.set_value(3)
        self.already_moved_once = False

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
        self.already_moved_once = False


class Rook(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("Rook")
        self.set_colour(colour)
        self.set_value(5)
        self.already_moved_once = False


class Queen(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("Queen")
        self.set_colour(colour)
        self.set_value(9)
        self.already_moved_once = False


class King(Piece):
    def __init__(self, colour):
        super().__init__()

        self.set_name("King")
        self.set_colour(colour)
        self.set_value(100)
        self.already_moved_once = False

        # A king move to a square with a 4 is only possible due to castling
        self.set_available_moves([[-1, 1, 1, 1, -1],
                                  [4, 1, 0, 1, 4],
                                  [-1, 1, 1, 1, -1]])
