import itertools

import numpy as np


class SudokuSolver:
    def __init__(self, board):
        """
        Takes a sudoku board as a numpy.ndarray, with empty squares represented
        by the number 0.
        """
        self.board = board.copy()
        self.history = list()
        self.pointer = (0, 0)
        self.num_steps = 0

    def solve(self):
        """
        Solves the Sudoku puzzle using depth-first search.
        """
        while self.board.astype(bool).sum() < 81:
            self.do_one_step()
            self.num_steps += 1

    def do_one_step(self):
        """
        Advances one step in the search. If the pointer is currently on a
        filled spot, advance the pointer. If the pointer is on an empty spot,
        attempt to add the first valid number between 1 and 9. If no numbers
        are valid, then reverse the previous number placement.
        """
        current_value = self.board[self.pointer]

        # If pointer is at a filled spot, advance the pointer
        if current_value != 0:
            self.advance_pointer()
            return

        # If pointer is at an empty space, attempt to add a number
        added_number = self.add_number()

        # If no valid number could be added, reverse previous moves
        if added_number == 0:
            self.revert_move()

    def valid_board(self):
        """
        Confirm that the board is valid
        """
        for i in range(1, 10):
            values = (self.board == i)
            if values.sum(axis=1).max() > 1 or values.sum(axis=0).max() > 1:
                return False

        for box_row, box_col in itertools.product(range(3), range(3)):
            box = self.get_box(box_row, box_col)
            for i in range(1, 10):
                if (box == i).sum() > 1:
                    return False
        return True

    def get_box(self, box_row, box_col):
        """
        Get a 3x3 box from the board, indexed by the box numbers.
        """
        return self.board[
            (3 * box_row):(3 * (box_row + 1)),
            (3 * box_col):(3 * (box_col + 1))
        ]

    def advance_pointer(self):
        """
        Advances the pointer from top left to bottom right.
        """
        if self.pointer[1] < 8:
            self.pointer = (self.pointer[0], self.pointer[1] + 1)
        else:
            self.pointer = (self.pointer[0] + 1, 0)

    def add_number(self):
        """
        Add a valid number, if possible. If no number 1-9 results in a valid
        board, then set the number to 0.
        """
        for i in range(1, 10):
            self.board[self.pointer] = i
            if self.valid_board():
                self.history.append({
                    'row': self.pointer[0],
                    'col': self.pointer[1],
                    'val': i
                })
                return i

        self.board[self.pointer] = 0
        return 0

    def revert_move(self):
        """
        Undo the previous move. If the previous move was the placement of a
        number < 9, then advance that number. If the previous move was the
        placement of a number 9, then that indicates the previous spot was
        also not valid. Then set the previous spot to zero also and reverse
        the pointer.
        """
        assert self.board[self.pointer] == 0

        previous_move = self.history[-1]
        self.history = self.history[:-1]

        # Reverse pointer to spot of previous move
        previous_pointer = (previous_move['row'], previous_move['col'])
        current_value = self.board[previous_pointer]

        if current_value < 9:
            self.board[previous_pointer] += 1
            self.history.append({
                'row': previous_move['row'],
                'col': previous_move['col'],
                'val': self.board[previous_pointer],
            })
        else:
            self.pointer = previous_pointer
            self.board[self.pointer] = 0
            self.revert_move()
