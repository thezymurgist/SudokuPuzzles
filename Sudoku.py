"""
This program generates a sodoku board based on the user's
selected difficulty and varifies whether or not the user has solved it correctly.
The board is printed to the screen after each move.

-Zym - January 2018
"""
import random

#eventually, this will take arguments that determine the size of the board and its difficulty
board = []
def generate_board():
    working_row = []
    for x in range (9):
        working_row.append(random.sample(range(1, 10))
    board.append(working_row)
    print board