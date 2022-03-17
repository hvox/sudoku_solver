from string import digits


def skip(it, ignored_value):
    for elem in it:
        if elem != ignored_value:
            yield elem


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
