# Author: Justin Quach-Law
# Date: 6/2/2021
# Description: “Kuba” is a 7x7 board game with white, black, and neutral marbles. One player is white and
# the other player is black. The objective is to either eliminate 7 neutrals or eliminate all of your
# opponent’s marbles.


class KubaGame:
    """A game of Kuba has an objective of either pushing off 7 red marbles or
     all of your opponent's marbles. In order to make a move with your marble,
     there needs to be an empty space or edge of the board from the side you
     are pushing. No diagonal pushes. Cannot undo a move your opponent just
     made last turn. A player who runs out of legal moves loses the game."""

    def __init__(self, p1_color, p2_color):
        """Initializes the 7x7 starting board of White, Black and Red marbles.
        Initializes player's turn and winner to None. Initializes red marbles
        captured to zero and black and white marbles to 8. Initializes player's
        name to marble's color. Takes parameters of two tuples containing
        player's name and their respective marble color."""
        self._board = make_board()
        self._players = init_players(p1_color, p2_color)
        self._winner = None
        self._turn = None
        self._previous_coord = None
        self._white = 8
        self._black = 8

    def get_current_turn(self):
        """Returns the player's name whose turn it is. Returns None if no
        player has made the first move. Takes no parameter."""
        return self._turn

    def get_winner(self):
        """Returns the name of the winner. Returns None if no player
        has won yet."""
        return self._winner

    def get_captured(self, name):
        """Returns the number of Red marbles captured by the player. Takes
        player's name as parameter. Returns 0 if no marble is captured."""
        return self._players[name][1]

    def get_marble(self, coord):
        """Returns the marble that is present at a location. Takes the coordinates
        of a cell as a tuple as parameter. Returns 'X' if no marble is present."""
        return self._board[coord]

    def get_marble_count(self):
        """Returns the number of White, Black and Red marbles as tuple in
        the order (W,B,R)."""
        white = 0
        black = 0
        red = 0
        for marble in list(self._board.values()):
            if marble == 'W':
                white += 1
            if marble == 'B':
                black += 1
            if marble == 'R':
                red += 1
        return white, black, red

    def get_board(self):
        """Returns the list of neighborhood pet(s)"""
        return self._board

    def make_move(self, name, coord, direction):
        """Makes a move with parameters of the player's name, the coordinate of
        to-be-moved marble, and the direction of the push. Returns True if
        move is successful, returns False otherwise."""
        if self.validate_move(name, coord, direction) is False:
            return False

        if direction == "R":
            if self.move_right(name, coord) is False:
                return False
        if direction == "L":
            if self.move_left(name, coord) is False:
                return False
        if direction == "B":
            if self.move_backward(name, coord) is False:
                return False
        if direction == "F":
            if self.move_forward(name, coord) is False:
                return False

        # save last coordinate move
        self._previous_coord = coord

        # check winner - red marbles captured
        if self._players[name][1] == 7:
            self._winner = name

        # check winner - black marbles
        if self._black == 0:
            if 'B' == self._players[list(self._players.keys())[0]][0]:
                self._winner = list(self._players.keys())[1]
            else:
                self._winner = list(self._players.keys())[0]

        # check winner - white marbles
        if self._white == 0:
            if 'W' == self._players[list(self._players.keys())[0]][0]:
                self._winner = list(self._players.keys())[1]
            else:
                self._winner = list(self._players.keys())[0]

        # update turn
        if name == list(self._players.keys())[1]:
            self._turn = list(self._players.keys())[0]
        else:
            self._turn = list(self._players.keys())[1]
        return True

    def move_left(self, name, coord):
        """Helps move function move left"""
        end_coord = coord

        # move starting point to left-end
        if end_coord[1] > 0:
            end_coord = (coord[0], coord[1] - 1)
            while self._board[end_coord] != 'X' and end_coord[1] != 0:
                end_coord = (coord[0], end_coord[1] - 1)

        # check last move coordinate
        if end_coord == self._previous_coord:
            return False

        # if start or reach left-end edge
        if end_coord[1] == 0:
            if self._board[end_coord] == "R":
                self._players[name][1] += 1
            if self._board[end_coord] == "B":
                self._black -= 1
            if self._board[end_coord] == "W":
                self._white -= 1

        # replacing backward by moving right
        end_num = end_coord[1]
        while coord[1] >= end_coord[1]:
            end_num += 1
            previous = (coord[0], end_num)
            if previous[1] > 6:
                self._board[end_coord] = "X"
            else:
                self._board[end_coord] = self._board[previous]
            end_coord = previous

        return True

    def move_right(self, name, coord):
        """Helps move function move right"""
        end_coord = coord

        # move starting point to right-end
        if end_coord[1] < 6:
            end_coord = (coord[0], coord[1] + 1)
            while self._board[end_coord] != 'X' and end_coord[1] != 6:
                end_coord = (coord[0], end_coord[1] + 1)

        # check last move coordinate
        if end_coord == self._previous_coord:
            return False

        # if start or reach right-end edge
        if end_coord[1] == 6:
            if self._board[end_coord] == "R":
                self._players[name][1] += 1
            if self._board[end_coord] == "B":
                self._black -= 1
            if self._board[end_coord] == "W":
                self._white -= 1

        # replacing backward by moving left
        end_num = end_coord[1]
        while coord[1] <= end_coord[1]:
            end_num -= 1
            previous = (coord[0], end_num)
            if previous[1] < 0:
                self._board[end_coord] = "X"
            else:
                self._board[end_coord] = self._board[previous]
            end_coord = previous

        return True

    def move_backward(self, name, coord):
        """Helps move function move backward"""
        end_coord = coord
        # move starting point to bottom-end
        if end_coord[0] < 6:
            end_coord = (coord[0] + 1, coord[1])
            while self._board[end_coord] != 'X' and end_coord[0] != 6:
                end_coord = (end_coord[0] + 1, end_coord[1])

        # check last move coordinate
        if end_coord == self._previous_coord:
            return False

        # if start or reach bottom-end edge
        if end_coord[0] == 6:
            if self._board[end_coord] == "R":
                self._players[name][1] += 1
            if self._board[end_coord] == "B":
                self._black -= 1
            if self._board[end_coord] == "W":
                self._white -= 1

        # replacing backward by moving forward
        end_num = end_coord[0]
        while coord[0] <= end_coord[0]:
            end_num -= 1
            previous = (end_num, coord[1])
            if previous[0] < 0:
                self._board[end_coord] = "X"
            else:
                self._board[end_coord] = self._board[previous]
            end_coord = previous

        return True

    def move_forward(self, name, coord):
        """Helps move function move forward"""
        end_coord = coord
        # move starting point to top-end
        if end_coord[0] > 0:
            end_coord = (coord[0] - 1, coord[1])
            while self._board[end_coord] != 'X' and end_coord[0] != 0:
                end_coord = (end_coord[0] - 1, end_coord[1])

        # check last move coordinate
        if end_coord == self._previous_coord:
            return False

        # if start or reach top-end edge
        if end_coord[0] == 0:
            if self._board[end_coord] == "R":
                self._players[name][1] += 1
            if self._board[end_coord] == "B":
                self._black -= 1
            if self._board[end_coord] == "W":
                self._white -= 1

        # replacing backward by moving backward
        end_num = end_coord[0]
        while coord[0] >= end_coord[0]:
            end_num += 1
            previous = (end_num, coord[1])
            if previous[0] > 6:
                self._board[end_coord] = "X"
            else:
                self._board[end_coord] = self._board[previous]
            end_coord = previous

        return True

    def validate_move(self, name, coord, direction):
        """Helps make_move function validate whether a move is valid. Returns
        True if move is valid, and false if move is invalid. Takes the parameters
        of the player's name, the coordinate of the to-be-moved marble, and the
        direction of the push."""
        if coord[0] < 0 or coord[0] > 6:  # if not in range
            return False
        if coord[1] < 0 or coord[1] > 6:  # if not in range
            return False
        if self._winner is not None:  # if theres a winner
            return False
        if self._players[name][0] != self._board[coord]:  # not player's marble
            return False
        if self._turn is not None and name != self._turn:  # move out of turn
            return False
        if direction == "R":
            previous = (coord[0], coord[1] - 1)
            if previous[1] < 0:  # check edge
                return True
            if self._board[previous] != "X":  # if previous not empty
                return False
        if direction == "L":
            previous = (coord[0], coord[1] + 1)
            if previous[1] > 6:  # check edge
                return True
            if self._board[previous] != "X":  # if previous not empty
                return False
        if direction == "B":
            previous = (coord[0] - 1, coord[1])
            if previous[0] < 0:  # check edge
                return True
            if self._board[previous] != "X":  # if previous not empty
                return False
        if direction == "F":
            previous = (coord[0] + 1, coord[1])
            if previous[0] > 6:  # check edge
                return True
            if self._board[previous] != "X":  # if previous not empty
                return False

        return True


def make_board():
    """Creates a Kuba game board"""
    board = dict()
    x = 0
    y = 0
    marble = "X"

    # initialize an 7x7 empty board
    n = 1
    while n <= 49:
        board[(x, y)] = marble
        if y == 6:
            x += 1
            y = 0
        else:
            y += 1
        n += 1

    # initialize top-left 4 white marbles
    board_corners(0, 0, "W", board)

    # initialize bottom-right 4 white marbles
    board_corners(5, 5, "W", board)

    # initialize bottom-left 4 black marbles
    board_corners(0, 5, "B", board)

    # initialize top-left 4 black marbles
    board_corners(5, 0, "B", board)

    # initialize middle red marbles
    board_red(3, 3, "R", board)

    return board


def board_corners(x_axis, y_axis, marble, board):
    """Helps make_board initialize both white and black marbles"""
    board[(x_axis, y_axis)] = marble
    board[(x_axis, y_axis + 1)] = marble
    board[(x_axis + 1, y_axis)] = marble
    board[(x_axis + 1, y_axis + 1)] = marble


def board_red(x_axis, y_axis, marble, board):
    """Helps make_board initialize red marbles"""
    # center
    board[(x_axis, y_axis)] = marble

    # vertical red marbles
    board[(x_axis - 1, y_axis)] = marble
    board[(x_axis - 2, y_axis)] = marble
    board[(x_axis + 1, y_axis)] = marble
    board[(x_axis + 2, y_axis)] = marble

    # horizontal red marbles
    board[(x_axis, y_axis - 1)] = marble
    board[(x_axis, y_axis - 2)] = marble
    board[(x_axis, y_axis + 1)] = marble
    board[(x_axis, y_axis + 2)] = marble

    # diagonal red marbles
    board[(x_axis + 1, y_axis + 1)] = marble
    board[(x_axis - 1, y_axis - 1)] = marble
    board[(x_axis + 1, y_axis - 1)] = marble
    board[(x_axis - 1, y_axis + 1)] = marble


def init_players(p1_color, p2_color):
    """Initializes player to marble and number of red captured"""
    players = dict()
    # player name: [marble color, red captured]
    players[p1_color[0]] = [p1_color[1], 0]
    players[p2_color[0]] = [p2_color[1], 0]
    return players
