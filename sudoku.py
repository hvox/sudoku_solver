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
    for x, y in skip(chain(row, col, square), (x0, y0)):
        table[x][y] = table[x][y] - {value}
        if not len(table[x][y]):
            return None
    return table


def traspose(matrix):
    new_matrix = list(map(list, matrix))
    for y in range(len(matrix)):
        for x in range(len(matrix)):
            new_matrix[x][y] = matrix[y][x]
    return new_matrix


def print_matrix_as_ascii_art(matrix):
    p = (
        lambda x: "".join(map(str, x)).rjust(4)
        if isinstance(x, set)
        else str(x)
    )
    for row in matrix:
        print(*map(p, row))
