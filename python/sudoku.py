from itertools import chain, product, repeat
from string import digits


def skip(it, ignored_value):
    for elem in it:
        if elem != ignored_value:
            yield elem


def set_value(table, x0, y0, value):
    if value not in table[x0][y0]:
        return None
    X0, Y0 = map(lambda x: (x // 3) * 3, (x0, y0))
    square = [(X0 + x, Y0 + y) for x, y in product(range(3), repeat=2)]
    row = zip(range(9), repeat(y0))
    col = zip(repeat(x0), range(9))
    table = [list(row) for row in table]
    table[x0][y0] = {value}
    updated_cells = []
    for x, y in skip(chain(row, col, square), (x0, y0)):
        if value in table[x][y]:
            table[x][y] = table[x][y] - {value}
            if not len(table[x][y]):
                return None
            if len(table[x][y]) == 1:
                updated_cells.append((x, y, next(iter(table[x][y]))))
    for x, y, value in updated_cells:
        table = set_value(table, x, y, value) if table else None
    return table


def traspose(matrix):
    new_matrix = list(map(list, matrix))
    for y in range(len(matrix)):
        for x in range(len(matrix)):
            new_matrix[x][y] = matrix[y][x]
    return new_matrix


def dp(table):
    minimal_set_size = 10
    minimal_cell = None
    for x, y in product(range(9), repeat=2):
        if len(table[x][y]) != 1 and len(table[x][y]) < minimal_set_size:
            minimal_set_size, minimal_cell = len(table[x][y]), (x, y)
    if minimal_cell is None:
        return [[cell for cell in row] for row in table]
    x, y = minimal_cell
    for guess in sorted(table[x][y]):
        if new_table := set_value(table, x, y, guess):
            if result := dp(new_table):
                return result
    return None


def print_matrix_as_ascii_art(matrix):
    p = (
        lambda x: "".join(map(str, x)).rjust(4)
        if isinstance(x, set)
        else str(x)
    )
    for row in matrix:
        print(*map(p, row))


def solve_sudoku(table):
    digits = set(range(1, 10))
    inner_table = [[digits for col in range(9)] for row in range(9)]
    for x, y in product(range(9), repeat=2):
        value = table[x][y]
        if value in digits:
            if not (inner_table := set_value(inner_table, x, y, value)):
                raise Exception(f"Contradiction at {x} {y}")
    return [[next(iter(cell)) for cell in row] for row in dp(inner_table)]


def sudoku(P):
    for row, col in [(r, c) for r in range(9) for c in range(9) if not P[r][c]]:
        rr, cc = (row // 3) * 3, (col // 3) * 3
        use = {1,2,3,4,5,6,7,8,9} - ({P[row][c] for c in range(9)} | {P[r][col] for r in range(9)} | {P[rr+r][cc+c] for r in range(3) for c in range(3)})
        if len(use) == 1:
            P[row][col] = use.pop()
            return sudoku(P)
    return P


def string_to_sudoku_table(string):
    str2digit = lambda x: int(x) if x in digits else 0
    lines = string.replace(" ", "").strip().split("\n")
    return [list(map(str2digit, r.strip())) for r in lines]
