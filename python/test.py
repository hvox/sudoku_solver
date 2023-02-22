from sudoku import solve_sudoku
from sudoku import string_to_sudoku_table
from sudoku import print_matrix_as_ascii_art

sudokus = {}
sudokus["simple example"] = string_to_sudoku_table(
    """
8 . . 5 . . 9 . .
. 4 . . 6 . . 7 .
7 . . 3 . . . . 2
1 . . . . . 2 . .
. 9 . . 3 . . 4 .
2 . . . . . . . 5
6 . . 9 . . . . .
. . . . 2 . . 3 .
4 . . 1 . . . . 9
"""
)

sudokus["empty table"] = string_to_sudoku_table(
    """
.........
.........
.........
.........
.........
.........
.........
.........
.........
"""
)

sudokus["simple example"] = string_to_sudoku_table(
    """
....45...
....26...
....9..37
4..9...8.
915......
......1..
.32...65.
7.....2..
...16..4.
"""
)


sudokus["example from web"] = string_to_sudoku_table(
    """
.....947.
..2.3..98
.6...2..1
......5.7
.7.....6.
8.3......
6..1...2.
74..6.9..
.194.....
"""
)

sudokus["world's hardest sudoky"] = string_to_sudoku_table(
    """
8........
..36.....
.7..9.2..
.5...7...
....457..
...1...3.
..1....68
..85...1.
.9....4..
"""
)

from time import time

for name, sudoku in sudokus.items():
    print(f"--------{name:-<72}")
    print_matrix_as_ascii_art(sudoku)
    t0 = time()
    solved_sudoku = solve_sudoku(sudoku)
    dt = time() - t0
    print("solved:")
    print_matrix_as_ascii_art(solved_sudoku)
    print("time spent:", dt)
