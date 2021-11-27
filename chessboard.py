import copy
from pieces import Pawn, Knight, Bishop, Rook, Queen, King


# Stores all the information for each instance of a chess game
class Chessboard:
    def __init__(self):
        self.chessboard = [
            [Rook(0), Knight(0), Bishop(0), Queen(0),
             King(0), Bishop(0), Knight(0), Rook(0)],
            [Pawn(0), Pawn(0), Pawn(0), Pawn(0), Pawn(0),
             Pawn(0), Pawn(0), Pawn(0)],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [Pawn(1), Pawn(1), Pawn(1), Pawn(1), Pawn(1),
             Pawn(1), Pawn(1), Pawn(1)],
            [Rook(1), Knight(1), Bishop(1), Queen(1),
             King(1), Bishop(1), Knight(1), Rook(1)]]

        self._history = []

    # Gets the element of the chessboad with the specific coordinate
    def get_square(self, coord):
        return self.chessboard[coord[1]][coord[0]]

    def get_history(self):
        return self._history

    def append_history(self, previous_square, new_square):
        notation1 = self.coord_to_notation(previous_square)
        notation2 = self.coord_to_notation(new_square)

        self._history.append({notation1} + {notation2})

    # Takes in two coordinates, moves the piece from the previous square to the new_square and then sets the previous square value to 0
    def move(self, previous_square, new_square):
        # print(previous_square, new_square)

        piece = self.chessboard[previous_square[1]][previous_square[0]]
        self.chessboard[previous_square[1]][previous_square[0]] = 0
        self.chessboard[new_square[1]][new_square[0]] = piece

    # Moves a piece to a different square, and takes into consideration special moves such as enpassant and castling
    def move_and_special_moves(self, coord1, coord2, special_move):
        colour = self.get_square(coord1).get_colour()

        self.move(coord1, coord2)

        x2, y2 = coord2

        # en passant
        if special_move == 3:
            if colour == 0:
                self.chessboard[y2 - 1][x2] = 0

            elif colour == 1:
                self.chessboard[y2 + 1][x2] = 0

        # castling
        elif special_move == 4:
            if x2 < 4:
                self.move((0, y2), (x2+1, y2))

            else:
                self.move((7, y2), (x2-1, y2))

    # returns all the legal moves a piece can make and takes into consideration self discovered checks
    def get_all_legal_moves(self, coord1):
        piece1 = self.get_square(coord1)

        legal_moves = []

        if piece1 != 0:
            legal_moves.extend(self.legal_specific_move(coord1))
            legal_moves.extend(self.legal_directional_move(coord1))

            legal_moves = self.remove_checks(coord1, legal_moves)

        return legal_moves

    # Removes the moves that would lead to a self discovered check
    def remove_checks(self, coord1, legal_moves):
        legal_moves_without_checks = []
        colour = self.get_square(coord1).get_colour()

        if colour == 0:
            initial = "w"
        else:
            initial = "b"

        original_chessboard = copy.deepcopy(self.chessboard)

        for coord2, special_move in legal_moves:
            attacked_squares = []

            self.move_and_special_moves(coord1, coord2, special_move)

            for y, row in enumerate(self.chessboard):
                for x, square in enumerate(row):
                    if square != 0 and square.get_colour() != colour:
                        attacked_squares.extend(
                            self.legal_specific_move((x, y)))
                        attacked_squares.extend(
                            self.legal_directional_move((x, y)))

            attacked_squares = set(attacked_squares)

            for y, row in enumerate(self.chessboard):
                for x, square in enumerate(row):
                    if str(square) == initial+"K":
                        king_coordinate = (x, y)
                        break

            if king_coordinate not in [attacked_square[0] for attacked_square in attacked_squares]:
                legal_moves_without_checks.append(coord2)

            self.chessboard = copy.deepcopy(original_chessboard)

        return legal_moves_without_checks

    # Returns a list of legal moves that the bishop, rook, or queen can make
    def legal_directional_move(self, coord):
        square1 = self.get_square(coord)
        x, y = coord
        straight, diagonally, _ = square1.get_all_moves()
        legal_moves = []

        direction_signs = []

        if straight:
            direction_signs.extend([(1, 0), (-1, 0), (0, 1), (0, -1)])

        if diagonally:
            direction_signs.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])

        for directions in direction_signs:
            x, y = coord
            x += 1 * directions[0]
            y += 1 * directions[1]

            while 0 <= x <= 7 and 0 <= y <= 7:
                coord2 = (x, y)
                square2 = self.get_square(coord2)

                if square2 == 0:
                    legal_moves.append((coord2, None))
                else:
                    if square1.get_colour() != square2.get_colour():
                        legal_moves.append((coord2, None))

                    break

                x += 1 * directions[0]
                y += 1 * directions[1]

        return legal_moves

    # Returns a list of legal specific moves the pawn, knight, and king can make
    def legal_specific_move(self, coord):
        square1 = self.get_square(coord)
        available_moves = square1.get_available_moves()
        x_square1, y_square1 = coord
        x_moves_center, y_moves_center = (0, 0)

        legal_moves = []

        for num_row, row in enumerate(available_moves):
            for num_column, item in enumerate(row):
                if item == 0:
                    x_moves_center = num_column
                    y_moves_center = num_row

        x_diff = x_square1 - x_moves_center
        y_diff = y_square1 - y_moves_center

        for num_row, row in enumerate(available_moves):
            for num_column, value in enumerate(row):
                coord2 = (num_column + x_diff, num_row+y_diff)

                if value != -1 and 7 >= (coord2[0]) >= 0 and 7 >= (coord2[1]) >= 0:
                    square2 = self.get_square(coord2)

                    legal = False

                    match value:
                        case 1:
                            legal = self.case_1(square1, square2)

                        case 2:
                            legal = self.can_pawn_double_step(square1, coord)

                        case 3:
                            legal = self.can_pawn_capture(
                                square1, square2, coord2)

                        case 4:
                            legal = self.can_castle(square1, coord)

                    if legal:
                        legal_moves.append((coord2, value))

        return legal_moves

    # Checks if a piece can do a 'value 1' move (knight move, king single square move, and pawn single move forwards)
    @staticmethod
    def case_1(square1, square2):
        if square1.get_name() == "Pawn" and square2 == 0:
            return True

        if square2 == 0:
            return True

        if square1.get_colour() != square2.get_colour():
            return True

        return False

    # Checks if a pawn can do a double step move
    def can_pawn_double_step(self, square, coord):
        x, y = coord
        colour = square.get_colour()

        if square.get_already_moved():
            return False

        if colour == 0:
            sign = 1
        else:
            sign = -1

        for i in range(1, 3):
            if self.get_square((x, y+(sign*i))) != 0:
                return False

        return True

    # Checks if a pawn can capture a piece
    def can_pawn_capture(self, square1, square2, coord2):
        if square2 != 0:
            if square1.get_colour() != square2.get_colour():
                return True

            return self.can_enpassant(square2, coord2)

        return False

    # check if a pawn can do the 'en passant' move
    def can_enpassant(self, square, coord2):
        history = self.get_history()
        colour = square.get_colour()
        x, y = coord2

        if colour == 0:
            i = -1
        else:
            i = 1

        last_move = (history or [None])[-1]
        under_square = self.get_square((x, y+i))

        if last_move != self.coord_to_notation((x, y+3*i)) + self.coord_to_notation((x, y+i)):
            return False

        if under_square != 0:
            if under_square.get_name() == "Pawn" and under_square.get_colour() != colour:
                if under_square.get_double_step():
                    return True

        return False

    # Checks if King can castle
    def can_castle(self, square, coord):
        x, y = coord

        if not square.get_already_moved():
            if x < 4:
                for i in range(1, x):
                    if self.get_square((x-i, y)) != 0:
                        return False

                rook = self.get_square((0, y))

                if not rook.get_already_moved():
                    return True
            else:
                for i in range(1, 7-x):
                    if self.get_square((x+i, y)) != 0:
                        return False

                rook = self.get_square((7, y))

                if not rook.get_already_moved():
                    return True

        return False

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

        return x_axis[x] + str(y+1)


if __name__ == "__main__":

    chess = Chessboard()

    # print(chess)

    # chess.move((0, 0), (4, 3))
    # print(chess)

    # current_square = chess.notation_to_coord("d1")
    # next_square = chess.notation_to_coord("d5")
    chess.move(chess.notation_to_coord("d1"), chess.notation_to_coord("d4"))
    chess.move(chess.notation_to_coord("e2"), chess.notation_to_coord("f3"))
    chess.move(chess.notation_to_coord("a8"), chess.notation_to_coord("e6"))
    print(chess)

    for num_row, row in enumerate(chess.chessboard):
        for num_column, _ in enumerate(row):
            coord = (num_column, num_row)
            square = chess.get_square(coord)
            if square != 0:
                # print(coord, square)
                legal_moves = chess.get_all_legal_moves(coord)

                print(f"{square} {legal_moves}")
