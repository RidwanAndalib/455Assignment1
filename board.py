"""
board.py

Implements a basic Go board with functions to:
- initialize to a given board size
- check if a move is legal
- play a move

The board uses a 1-dimensional representation with padding
"""

import numpy as np
from board_util import (
    GoBoardUtil,
    BLACK,
    WHITE,
    EMPTY,
    BORDER,
    PASS,
    is_black_white,
    is_black_white_empty,
    coord_to_point,
    where1d,
    MAXSIZE,
    GO_POINT
)

"""
The GoBoard class implements a board and basic functions to play
moves, check the end of the game, and count the acore at the end.
The class also contains basic utility functions for writing a Go player.
For many more utility functions, see the GoBoardUtil class in board_util.py.

The board is stored as a one-dimensional array of GO_POINT in self.board.
See GoBoardUtil.coord_to_point for explanations of the array encoding.
"""
class GoBoard(object):
    def __init__(self, size):
        """
        Creates a Go board of given size
        """
        assert 2 <= size <= MAXSIZE
        self.reset(size)

    def reset(self, size):
        """
        Creates a start state, an empty board with given size.
        """
        self.size = size
        self.NS = size + 1
        self.WE = 1
        self.ko_recapture = None
        self.last_move = None
        self.last2_move = None
        self.current_player = BLACK
        self.maxpoint = size * size + 3 * (size + 1)
        self.board = np.full(self.maxpoint, BORDER, dtype=GO_POINT)
        self._initialize_empty_points(self.board)

    def copy(self):
        b = GoBoard(self.size)
        assert b.NS == self.NS
        assert b.WE == self.WE
        b.ko_recapture = self.ko_recapture
        b.last_move = self.last_move
        b.last2_move = self.last2_move
        b.current_player = self.current_player
        assert b.maxpoint == self.maxpoint
        b.board = np.copy(self.board)
        return b

    def get_color(self, point):
        return self.board[point]

    def pt(self, row, col):
        return coord_to_point(row, col, self.size)

    def is_legal(self, point, color):
        """
        Check whether it is legal for color to play on point
        This method tries to play the move on a temporary copy of the board.
        This prevents the board from being modified by the move
        """
        return color == self.current_player

    def get_empty_points(self):
        """
        Return:
            The empty points on the board
        """
        return where1d(self.board == EMPTY)

    def get_occupied_points(self):
        """
        Return:
            The occupied points on the board
        """
        points = []
        for point in where1d(self.board == BLACK):
            points.append(point)
        for point in where1d(self.board == WHITE):
            points.append(point)
        return points

    def check_win(self):
        points = self.get_occupied_points()
        for point in points:
            color = self.get_color(point)
            if self.isVerticalWin(point) or self.isHorizontalWin(point) or self.isDiag1Win(point) or self.isDiag2Win(point):
                return color
        return 0
    
    def isVerticalWin(self, point):
        p5 = point
        p4 = p5 - self.NS
        p3 = p4 - self.NS
        p2 = p3 - self.NS
        p1 = p2 - self.NS
        p6 = p5 + self.NS
        p7 = p6 + self.NS
        p8 = p7 + self.NS
        p9 = p8 + self.NS
        if p1 >= 0:
            if self.get_color(p1)==self.get_color(p5) and self.get_color(p2)==self.get_color(p5) and self.get_color(p3)==self.get_color(p5) and self.get_color(p4)==self.get_color(p5):
                return True
        if p9 <= self.NS*self.NS:
            if self.get_color(p6)==self.get_color(p5) and self.get_color(p7)==self.get_color(p5) and self.get_color(p8)==self.get_color(p5) and self.get_color(p9)==self.get_color(p5):
                return True
        return False
        
    def isHorizontalWin(self, point):
        p5 = point
        p4 = p5 - 1
        p3 = p4 - 1
        p2 = p3 - 1
        p1 = p2 - 1
        p6 = p5 + 1
        p7 = p6 + 1
        p8 = p7 + 1
        p9 = p8 + 1
        if p1 >= 0:
            if self.get_color(p1)==self.get_color(p5) and self.get_color(p2)==self.get_color(p5) and self.get_color(p3)==self.get_color(p5) and self.get_color(p4)==self.get_color(p5):
                return True
        if p9 <= self.NS*self.NS:
            if self.get_color(p6)==self.get_color(p5) and self.get_color(p7)==self.get_color(p5) and self.get_color(p8)==self.get_color(p5) and self.get_color(p9)==self.get_color(p5):
                return True
        return False

    def isDiag1Win(self, point):
        p5 = point
        p4 = p5 - self.NS - 1
        p3 = p4 - self.NS - 1
        p2 = p3 - self.NS - 1
        p1 = p2 - self.NS - 1
        p6 = p5 + self.NS + 1
        p7 = p6 + self.NS + 1
        p8 = p7 + self.NS + 1
        p9 = p8 + self.NS + 1

        if p1 >= 0:
            if self.get_color(p1)==self.get_color(p5) and self.get_color(p2)==self.get_color(p5) and self.get_color(p3)==self.get_color(p5) and self.get_color(p4)==self.get_color(p5):
                return True
        if p9 <= self.NS*self.NS:
            if self.get_color(p6)==self.get_color(p5) and self.get_color(p7)==self.get_color(p5) and self.get_color(p8)==self.get_color(p5) and self.get_color(p9)==self.get_color(p5):
                return True
        return False


    def isDiag2Win(self, point):
        p5 = point
        p4 = p5 - self.NS + 1
        p3 = p4 - self.NS + 1
        p2 = p3 - self.NS + 1
        p1 = p2 - self.NS + 1
        p6 = p5 + self.NS - 1
        p7 = p6 + self.NS - 1
        p8 = p7 + self.NS - 1
        p9 = p8 + self.NS - 1
        print(p5, p4, p3, p2, p1)
        
        if p1 >= 0 and p1 <= self.NS*self.NS:
            if self.get_color(p1)==self.get_color(p5) and self.get_color(p2)==self.get_color(p5) and self.get_color(p3)==self.get_color(p5) and self.get_color(p4)==self.get_color(p5):
                return True
        if p9 >= 0 and p9 <= self.NS*self.NS:
            if self.get_color(p6)==self.get_color(p5) and self.get_color(p7)==self.get_color(p5) and self.get_color(p8)==self.get_color(p5) and self.get_color(p9)==self.get_color(p5):
                return True
        return False
    
    def row_start(self, row):
        assert row >= 1
        assert row <= self.size
        return row * self.NS + 1

    def _initialize_empty_points(self, board):
        """
        Fills points on the board with EMPTY
        Argument
        ---------
        board: numpy array, filled with BORDER
        """
        for row in range(1, self.size + 1):
            start = self.row_start(row)
            board[start : start + self.size] = EMPTY

    def is_eye(self, point, color):
        """
        Check if point is a simple eye for color
        """
        if not self._is_surrounded(point, color):
            return False
        # Eye-like shape. Check diagonals to detect false eye
        opp_color = GoBoardUtil.opponent(color)
        false_count = 0
        at_edge = 0
        for d in self._diag_neighbors(point):
            if self.board[d] == BORDER:
                at_edge = 1
            elif self.board[d] == opp_color:
                false_count += 1
        return false_count <= 1 - at_edge  # 0 at edge, 1 in center

    def _is_surrounded(self, point, color):
        """
        check whether empty point is surrounded by stones of color
        (or BORDER) neighbors
        """
        for nb in self._neighbors(point):
            nb_color = self.board[nb]
            if nb_color != BORDER and nb_color != color:
                return False
        return True

    def _has_liberty(self, block):
        """
        Check if the given block has any liberty.
        block is a numpy boolean array
        """
        for stone in where1d(block):
            empty_nbs = self.neighbors_of_color(stone, EMPTY)
            if empty_nbs:
                return True
        return False

    def _block_of(self, stone):
        """
        Find the block of given stone
        Returns a board of boolean markers which are set for
        all the points in the block 
        """
        color = self.get_color(stone)
        assert is_black_white(color)
        return self.connected_component(stone)

    def connected_component(self, point):
        """
        Find the connected component of the given point.
        """
        marker = np.full(self.maxpoint, False, dtype=bool)
        pointstack = [point]
        color = self.get_color(point)
        assert is_black_white_empty(color)
        marker[point] = True
        while pointstack:
            p = pointstack.pop()
            neighbors = self.neighbors_of_color(p, color)
            for nb in neighbors:
                if not marker[nb]:
                    marker[nb] = True
                    pointstack.append(nb)
        return marker

    def _detect_and_process_capture(self, nb_point):
        """
        Check whether opponent block on nb_point is captured.
        If yes, remove the stones.
        Returns the stone if only a single stone was captured,
        and returns None otherwise.
        This result is used in play_move to check for possible ko
        """
        single_capture = None
        opp_block = self._block_of(nb_point)
        if not self._has_liberty(opp_block):
            captures = list(where1d(opp_block))
            self.board[captures] = EMPTY
            if len(captures) == 1:
                single_capture = nb_point
        return single_capture

    def play_move(self, point, color):
        """
        Play a move of color on point
        Returns boolean: whether move was legal
        """
        assert is_black_white(color)
        
        if self.board[point] == EMPTY:
          self.board[point] = color
          self.current_player = GoBoardUtil.opponent(color)
          self.last2_move = self.last_move
          self.last_move = point
          return None
          
        return "occupied"

    def neighbors_of_color(self, point, color):
        """ List of neighbors of point of given color """
        nbc = []
        for nb in self._neighbors(point):
            if self.get_color(nb) == color:
                nbc.append(nb)
        return nbc

    def all_neighbors_of_color(self, point, color):
	    """ List all neighbors of point of given color """
	    nbc = []
	    neighbors = self._neighbors(point)
	    neighbors += self._diag_neighbors(point)
	    for point2 in neighbors:
	        if self.get_color(point2) == color:
	            nbc.append(point2)
	    return nbc

    def _neighbors(self, point):
        """ List of all four neighbors of the point """
        return [point - 1, point + 1, point - self.NS, point + self.NS]

    def _diag_neighbors(self, point):
        """ List of all four diagonal neighbors of point """
        return [
            point - self.NS - 1,
            point - self.NS + 1,
            point + self.NS - 1,
            point + self.NS + 1,
        ]

    def last_board_moves(self):
        """
        Get the list of last_move and second last move.
        Only include moves on the board (not None, not PASS).
        """
        board_moves = []
        if self.last_move != None and self.last_move != PASS:
            board_moves.append(self.last_move)
        if self.last2_move != None and self.last2_move != PASS:
            board_moves.append(self.last2_move)
            return 
