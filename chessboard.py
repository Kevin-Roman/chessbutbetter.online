from pieces import Bishop, King, Knight, Pawn, Queen, Rook


class Chessboard:
    """Stores all the information for each instance of a chessboard
    """

    def __init__(self):
        # configuration of the chessboard
        self.chessboard = [
            [Rook(1), Knight(1), Bishop(1), Queen(1),
             King(1), Bishop(1), Knight(1), Rook(1)],
            [Pawn(1), Pawn(1), Pawn(1), Pawn(1), Pawn(1),
             Pawn(1), Pawn(1), Pawn(1)],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [Pawn(0), Pawn(0), Pawn(0), Pawn(0), Pawn(0),
             Pawn(0), Pawn(0), Pawn(0)],
            [Rook(0), Knight(0), Bishop(0), Queen(0),
             King(0), Bishop(0), Knight(0), Rook(0)]]

        self.history = []

    def get_square(self, coord):
        """Gets the element of the chessboad with the specific coordinate

        Args:
            coord (tuple of (int, int)): tuple containing two numbers representing the x and the y value respectively.

        Returns:
            int/object: 0 representing an empty square or an instance of a Piece subclass if the square contains a piece.
        """
        return self.chessboard[coord[1]][coord[0]]

    def set_square(self, coord, new_value):
        """Sets the value/piece of the specific square on the chessboard

        Args:
            coord (tuple of (int, int)): tuple containing two numbers representing the x and the y value respectively.
            new_value (str/class): 0 or the piece object to be replaced on the selected square.
        """
        self.chessboard[coord[1]][coord[0]] = new_value

    def append_history(self, previous_square, new_square, piece_attributes, captured_piece, pawn_enpassant, rook_castling_move):
        """Appends data about the last move executed to the history list attribute

        Args:
            previous_square (tuple of (int, int)): tuple coordinate of the square that will be moved
            new_square (tuple of (int, int)): tuple coordinate of the square the piece will move to
            piece_attributes (dict): dictioanary containing attributes of the object
            captured_piece (int/class): 0 or instance of a Piece type class
            pawn_enpassant (NoneType/tuple of (tuple, class)): containing the coordinate and object of the pawn that was removed
            rook_castling_move (NoneType/tuple): containing the coordinate of the square the rook moved from
        """
        self.history.append((previous_square,
                             new_square,
                             piece_attributes,
                             captured_piece,
                             pawn_enpassant,
                             rook_castling_move))

    def move(self, previous_square, new_square):
        """Moves a piece from one square to another and sets the initial square to empty (0)

        Args:
            previous_square (tuple of (int, int)): tuple coordinate of the square that will be moved
            new_square (tuple of (int, int)): tuple coordinate of the square the piece will move to

        Returns:
            tuple of (dict, str/class): tuple containing dictionary of attributes of the piece object and the object itself.
        """
        captured_piece = self.get_square(new_square)

        piece = self.get_square(previous_square)

        # Creates a copy of the attributes of the piece and stores it into a variable
        moved_piece_attr = dict(piece.__dict__)

        self.set_square(new_square, piece)
        self.set_square(previous_square, 0)

        return moved_piece_attr, captured_piece

    def undo_move(self):
        """Undos the last move
        """
        old_square, current_square, piece_attributes, captured_piece, pawn_enpassant, rook_castling_move = self.history.pop()

        self.move(current_square, old_square)

        # set the square the piece moved to back to its original value
        self.set_square(current_square, captured_piece)

        if pawn_enpassant is not None:
            # Place back the captured enemy pawn
            self.set_square(pawn_enpassant[0], pawn_enpassant[1])

        elif rook_castling_move is not None:
            # Move the rook back to its previous position
            self.move(rook_castling_move[1], rook_castling_move[0])
            self.chessboard[rook_castling_move[0][1]
                            ][rook_castling_move[0][0]].already_moved = False

        # set attributes of the moved piece back to its previous state
        self.get_square(old_square).__dict__ = piece_attributes

    def move_and_special_moves(self, start_coord, end_coord, special_move):
        """Moves a piece to a different square and takes into consideration
            special moves such as enpassant and castling

        Args:
            start_coord (tuple of (int, int)): tuple coordinate of the square that be moved
            end_coord (tuple of (int, int)): tuple coordinate of the square the piece will move to
            special_move (int): the special move type
        """

        colour = self.get_square(start_coord).colour

        piece_attributes, captured_piece = self.move(start_coord, end_coord)

        x2, y2 = end_coord

        self.chessboard[y2][x2].already_moved = True

        pawn_enpassant = None
        rook_castling_move = None

        # en passant
        if special_move == 5:
            if colour == 0:
                pawn_enpassant_coord = (x2, y2+1)
                # pawn_enpassant = (coord, pawn object)
                pawn_enpassant = (pawn_enpassant_coord,
                                  self.get_square((x2, y2+1)))
                self.set_square(pawn_enpassant_coord, 0)

            elif colour == 1:
                pawn_enpassant_coord = (x2, y2-1)
                # pawn_enpassant = (coord, pawn object)
                pawn_enpassant = (
                    pawn_enpassant_coord, self.get_square((x2, y2-1)))
                self.set_square(pawn_enpassant_coord, 0)

        # castling
        elif special_move == 4:
            if x2 < 4:
                rook_castling_move = ((0, y2), (x2+1, y2))
                self.move(rook_castling_move[0], rook_castling_move[1])

            else:
                rook_castling_move = ((7, y2), (x2-1, y2))
                self.move(rook_castling_move[0], rook_castling_move[1])

        # promotion - promote the pawn to a Queen
        if self.get_square(end_coord) != 0 and self.get_square(end_coord).name == "Pawn":
            if colour == 0 and y2 == 0:
                self.set_square(end_coord, Queen(0))
                self.chessboard[y2][x2].already_moved = True

            elif colour == 1 and y2 == 7:
                self.set_square(end_coord, Queen(1))
                self.chessboard[y2][x2].already_moved = True

        # add latest move and other information required for undo to history list
        self.append_history(start_coord, end_coord, piece_attributes,
                            captured_piece, pawn_enpassant, rook_castling_move)

    def get_directional_moves(self, start_coord):
        """Gets all the possible directional moves a piece can make.

        Args:
            start_coord (tuple of (int, int)): a tuple coordinate

        Returns:
            list of tuple: containing the coordinates the piece can move to and the special move type
        """
        start_square = self.get_square(start_coord)
        possible_moves = []

        # list of tuple translations which represent the directions
        # in which the piece can move to.
        directions = []

        if start_square.straight:
            directions.extend([(1, 0), (-1, 0), (0, 1), (0, -1)])

        if start_square.diagonal:
            directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])

        for direction in directions:
            x, y = start_coord
            x += 1 * direction[0]
            y += 1 * direction[1]

            # stop when square is outside the chessboard boundary
            while 0 <= x <= 7 and 0 <= y <= 7:
                # add the translation to the current coordinate

                end_coord = (x, y)
                end_square = self.get_square(end_coord)

                # if square is empty then it is a possible move
                if end_square == 0:
                    possible_moves.append((end_coord, None))
                else:
                    # stop once there is a piece on the square
                    if start_square.colour != end_square.colour:
                        possible_moves.append((end_coord, None))

                    break

                # translate the coordinate by the direction
                x += 1 * direction[0]
                y += 1 * direction[1]

        return possible_moves

    def get_specific_moves(self, start_coord):
        """Gets all the possible specific moves the pawn, knight, and king can make.

        Args:
            coord (tuple of (int, int)): a tuple coordinate

        Returns:
            list of tuples: containing the coordinates the piece can move to and the special move type
        """
        start_square = self.get_square(start_coord)
        x_start_square, y_start_square = start_coord
        # coordinate of the starting square
        available_moves = start_square.available_moves
        # coordinate of the element 0 in the available_moves list
        x_relational_center, y_relational_center = (0, 0)

        possible_moves = []

        for num_row, row in enumerate(available_moves):
            for num_column, item in enumerate(row):
                if item == 0:
                    x_relational_center = num_column
                    y_relational_center = num_row
                    break
            else:  # no break
                continue

            break

        # the translation from the each element in available_moves
        # to its corresponding square in the chessboard.
        x_diff = x_start_square - x_relational_center
        y_diff = y_start_square - y_relational_center

        for num_row, row in enumerate(available_moves):
            for num_column, value in enumerate(row):
                end_coord = (num_column + x_diff, num_row + y_diff)
                # if square within the chessboard boundary
                if value not in [-1, 0] and 7 >= end_coord[0] >= 0 and 7 >= end_coord[1] >= 0:
                    end_square = self.get_square(end_coord)

                    possible = False

                    match value:
                        case 1:
                            possible = self.case_1(start_square, end_square)

                        case 2:
                            possible = self.can_pawn_double_step(
                                start_square, start_coord)

                        case 3:
                            possible = self.can_pawn_capture(
                                start_square, end_square)

                            if not possible:
                                possible = self.can_enpassant(
                                    start_square, end_coord)
                                if possible:
                                    value = 5

                        case 4:
                            possible = self.can_castle(
                                start_square, start_coord, end_coord)

                        case _:
                            raise ValueError(
                                "Special move type is not between -1 and 4 inclusively.")

                    if possible:
                        possible_moves.append((end_coord, value))

        return possible_moves

    @staticmethod
    def case_1(start_square, end_square):
        """Checks if a piece can make a value '1' move (knight move, king single square move, and pawn single move forwards)

        Args:
            start_square (int/object): the value of a square
            end_square (int/object): the value of a square

        Returns:
            bool: whether the move is legal or not
        """
        # if end_square is empty then the piece can move there.
        if end_square == 0:
            return True

        # if the piece that would be captured has the opposite colour of the player, then the move is possible.
        elif start_square.name != "Pawn" and start_square.colour != end_square.colour:
            return True

        return False

    def can_pawn_double_step(self, square, coord):
        """Checks if a pawn can do a double step move

        Args:
            square (int/object): the value of a square
            coord (tuple of (int, int)): the tuple coordinate of that square

        Returns:
            bool: whether the move is legal or not
        """
        x, y = coord
        colour = square.colour
        # pawn can execute double step only if it's its first move
        # in the game
        if square.already_moved:
            return False

        # the sign is determined by he colour of the piece
        # and will be used to check the the squares in front
        # of that piece
        if colour == 0:
            sign = -1
        else:
            sign = 1

        # checking if both squares in front of the piece are empty
        for i in range(1, 3):
            if self.get_square((x, y+(sign*i))) != 0:
                return False

        return True

    def can_pawn_capture(self, start_square, end_square):
        """Checks if a pawn can capture a piece

        Args:
            start_square (int/object): the value of initial square
            end_square (int/object): the value of square the piece
                would move to
            end_coord (tuple of (int, int)): coordinate of the square
                the piece would move to

        Returns:
            bool: whether the move is legal or not
        """
        if end_square != 0:
            if start_square.colour != end_square.colour:
                return True

        return False

    def can_enpassant(self, start_square, end_coord):
        """Checks if a pawn can do the 'en passant' move

        Args:
            start_square (int/object): the value of initial square
            end_coord (tuple of (int, int)): coordinate of the square
                the piece would move to

        Returns:
            bool: whether the move is legal or not
        """
        history = self.history
        colour = start_square.colour
        x, y = end_coord

        if colour == 0:
            i = 1
        else:
            i = -1

        last_move = (history or [None])[-1]

        if last_move is not None:
            # pylint: disable=E1136
            last_move = last_move[0:2]

        # checks if the last move in history was the opponent's pawn
        # double step move
        if last_move != ((x, y-i), (x, y+i)):
            return False

        # square under the opponent pawn (from the player's perspective)
        under_square = self.get_square((x, y+i))

        # en passant only is possible if the the there is an
        # opponent's pawn to the left/right of the player's pawn
        if under_square != 0:
            if under_square.name == "Pawn" and under_square.colour != colour:
                return True

        return False

    def can_castle(self, start_square, start_coord, end_coord):
        """Checks if King can castle

        Args:
            start_square (int/object): the square the King is on
            start_coord (tuple of (int, int)): the coordinate of the square the King is on
            end_coord (tuple of (int, int)): the coordinate of the square the King would move to

        Returns:
            bool: whether the move is legal or not
        """
        x1, y1 = start_coord
        x2, _ = end_coord

        if not start_square.already_moved:
            if x2 < 4:
                # check if all squares between the king and the
                # corresponding rook are empty
                for i in range(1, x1):
                    if self.get_square((x1-i, y1)) != 0:
                        return False

                rook = self.get_square((0, y1))
                # En passant can only occur if the corresponding rook
                # has not once during the game.
                if rook != 0 and not rook.already_moved:
                    return True
            else:
                for i in range(1, 7-x1):
                    if self.get_square((x1+i, y1)) != 0:
                        return False

                rook = self.get_square((7, y1))

                if rook != 0 and not rook.already_moved:
                    return True
        return False

    def remove_checks(self, start_coord, possible_moves):
        """Removes the moves that would lead to a self discovered check

        Args:
            start_coord (tuple of (int, int)): tuple coordinate of the square that the piece will be moved from
            possible_moves (list of tuple): containing the coordinates the piece can move to and the special move type

        Returns:
            list of tuple: containing the filtered coordinates the piece can move to and the special move type
        """
        start_square = self.get_square(start_coord)

        # used later when finding the king's coordinate
        if start_square.colour == 0:
            initial = "w"
        else:
            initial = "b"

        legal_moves = []

        for end_coord, special_move in possible_moves:
            attacked_squares = []

            self.move_and_special_moves(start_coord, end_coord, special_move)

            # get all the possible moves the opponent can make
            for y, row in enumerate(self.chessboard):
                for x, square in enumerate(row):
                    if square != 0 and square.colour != start_square.colour:
                        attacked_squares.extend(
                            self.get_specific_moves((x, y)))
                        attacked_squares.extend(
                            self.get_directional_moves((x, y)))

            # removes repeated elements
            attacked_squares = set(attacked_squares)

            # Check if squares for castling are not attacked
            if special_move == 4:
                can_castle = True
                x2, y2 = end_coord

                # check if the squares the king would move through and to are attacked by opposing pieces
                if x2 == 2:
                    for i in range(2, 5):
                        if (i, y2) in [attacked_square[0] for attacked_square in attacked_squares]:
                            can_castle = False

                elif x2 == 6:
                    for i in range(4, 7):
                        if (i, y2) in [attacked_square[0] for attacked_square in attacked_squares]:
                            # print(f"CASTLING: {(i, y2)}")
                            can_castle = False

                if can_castle:
                    legal_moves.append((end_coord, special_move))

            else:
                # get the coordinate of the player's king
                for y, row in enumerate(self.chessboard):
                    for x, square in enumerate(row):
                        if str(square) == initial+"K":
                            king_coordinate = (x, y)
                            break
                    else:  # no break
                        continue

                    break

                if king_coordinate not in [attacked_square[0] for attacked_square in attacked_squares]:
                    legal_moves.append((end_coord, special_move))

            # revert the chessboard back to its previous state
            self.undo_move()

        return legal_moves

    def get_legal_moves(self, start_coord):
        """Returns all the legal moves a piece can make and takes into consideration
            self discovered checks

        Args:
            start_coord (tuple of (int, int)): the coordinate the piece is moving from

        Returns:
            list of tuple: containing the legal coordinates the piece can move to and their special move type
        """
        start_square = self.get_square(start_coord)

        legal_moves = []
        possible_moves = []

        if start_square != 0:
            possible_moves.extend(self.get_specific_moves(start_coord))
            possible_moves.extend(self.get_directional_moves(start_coord))

            legal_moves = self.remove_checks(start_coord, possible_moves)

        return legal_moves

    def is_checkmate_or_draw(self, turn):
        """Checks whether the current player to move is in a checkmate or a draw

        Args:
            turn (int): 0 or 1 representing white or black side's turn respectively

        Returns:
            str: either 'checkmate' or 'draw'
        """
        legal_moves = []

        # get all the moves the player can make
        for num_row, row in enumerate(self.chessboard):
            for num_column, _ in enumerate(row):
                coord = (num_column, num_row)
                square = self.get_square(coord)
                if square != 0 and square.colour == turn:
                    unchecked_legal_moves = self.get_legal_moves(coord)
                    # 'unchecked_legal_moves != []' can be simplified to 'unchecked_legal_moves' as an empty sequence is false
                    if unchecked_legal_moves:
                        legal_moves.append(unchecked_legal_moves)

        # print(f"legal_moves: {legal_moves}")

        # Determines whether it is a checkmate or a stalemate
        if len(legal_moves) == 0:
            attacked_squares = []

            # get all the squares the opponent's pieces are attacking
            for y, row in enumerate(self.chessboard):
                for x, square in enumerate(row):
                    if square != 0 and square.colour != turn:
                        attacked_squares.extend(
                            self.get_specific_moves((x, y)))
                        attacked_squares.extend(
                            self.get_directional_moves((x, y)))

            # removing repeated values in the list by converting it into a set
            attacked_squares = set(attacked_squares)

            # find the coordinate of the king in the chessboard
            for y, row in enumerate(self.chessboard):
                for x, square in enumerate(row):
                    if square != 0 and square.colour == turn and str(square)[1] == "K":
                        king_coordinate = (x, y)
                        break
                else:  # no break
                    continue

                break

            # if king is attacked then it is checkmate
            if king_coordinate in [attacked_square[0] for attacked_square in attacked_squares]:
                return "checkmate"

            # if king is not attacked then it is a stalemate
            return "draw"

        return False

    def __str__(self):
        """Returns the string representation of the chessboard
        """

        str_chessboard = ""
        for x in range(8):
            # y-axis
            str_chessboard += f"{8-x}  "

            for y in range(8):
                piece_in_square = str(self.chessboard[x][y])

                str_chessboard += f'{piece_in_square}{" "*(3-len(piece_in_square))}'

            # add new line
            str_chessboard += "\n"

        # x-axis
        str_chessboard += "   a  b  c  d  e  f  g  h\n"

        return str_chessboard

    @staticmethod
    def notation_to_coord(notation):
        """Converts algebraic notation to tuple coordinate format (e.g. from "a1" to (0,0))

        Args:
            notation (str): algebraic coordinate

        Returns:
            tuple of (int, int)): tuple coordinate
        """

        x, y = list(notation)

        x_axis = {"a": 0, "b": 1, "c": 2, "d": 3,
                  "e": 4, "f": 5, "g": 6, "h": 7}

        return (x_axis[x], 8 - int(y))

    @staticmethod
    def coord_to_notation(coord):
        """Converts tuple coordinate format to algebraic notation (e.g. from (0,0)  to "a1")

        Args:
            coord (tuple of (int, int)): tuple coordinate

        Returns:
            str: algebraic coordinate
        """

        # pylint: disable=unbalanced-tuple-unpacking
        x, y = list(coord)

        x_axis = {0: "a", 1: "b", 2: "c", 3: "d",
                  4: "e", 5: "f", 6: "g", 7: "h"}

        return x_axis[x] + str(8 - y)


if __name__ == "__main__":

    chess = Chessboard()

    # for i in range(8):
    #     for j in range(8):
    #         chess.chessboard[i][j] = 0

    # print(chess)

    # chess.chessboard[0][0] = King(1)
    # chess.chessboard[1][5] = Queen(0)
    # chess.chessboard[2][1] = Queen(0)
    # chess.chessboard[6][3] = King(0)

    # print(chess)

    # print(chess.is_checkmate_or_draw(1))

    # chess.append_history(chess.notation_to_coord("d2"),
    #                      chess.notation_to_coord("d5"))

    # chess.append_history(chess.notation_to_coord("e4"),
    #                      chess.notation_to_coord("d7"))

    # print(chess.history)

    # chess.move_and_special_moves(chess.notation_to_coord(
    #     "c7"), chess.notation_to_coord("c1"), None)

    # chess.append_history(chess.notation_to_coord("d2"),
    #                      chess.notation_to_coord("d5"))

    # chess.move_and_special_moves(chess.notation_to_coord(
    #     "e7"), chess.notation_to_coord("e5"), 2)
    # chess.append_history(chess.notation_to_coord("e7"),
    #                      chess.notation_to_coord("e5"))

    # # prints out all the legal moves the wP on d5 can move to
    # print([chess.coord_to_notation(legal_move[0])
    #       for legal_move in chess.get_legal_moves(chess.notation_to_coord("d5"))])

    # print(chess)

    # chess.move_and_special_moves(chess.notation_to_coord(
    #     "d5"), chess.notation_to_coord("e6"), 3)

    # chess.append_history(chess.notation_to_coord("d5"),
    #                      chess.notation_to_coord("e6"))

    # print(chess)

    # for num_row, row in enumerate(chess.chessboard):
    #     for num_column, _ in enumerate(row):
    #         coord = (num_column, num_row)
    #         square = chess.get_square(coord)
    #         if square != 0:
    #             possible_moves = [chess.coord_to_notation(
    #                 possible_move[0]) for possible_move in chess.get_legal_moves(coord)]

    #             print(f"{square} {possible_moves}")
