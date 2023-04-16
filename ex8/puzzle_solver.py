import copy
from typing import *


def max_min_seen_up(picture: list[list[int]], row: int, col: int, max_or_min: int) -> int:
    """
    :param max_or_min: 0 is for max and 1 is for min
    :return: return the num of seen cells on the cells above
    """
    is_first_row = row < 0
    if max_or_min == 0:
        if picture[row][col] == 0 or is_first_row:
            return 0
    else:
        if picture[row][col] != 1 or is_first_row:
            return 0
    return 1 + max_min_seen_up(picture, row - 1, col, max_or_min)


def max_min_seen_down(picture: list[list[int]], row: int, col: int, max_or_min: int) -> int:
    """
    :param max_or_min: 0 is for max and 1 is for min
    :return: return the num of seen cells on the cells below
    """
    is_last_row = row >= len(picture)
    if max_or_min == 0:
        if is_last_row or picture[row][col] == 0:
            return 0
    else:
        if is_last_row or picture[row][col] != 1:
            return 0
    return 1 + max_min_seen_down(picture, row + 1, col, max_or_min)


def max_min_seen_left(picture: list[list[int]], row: int, col: int, max_or_min: int) -> int:
    """
    :param max_or_min: 0 is for max and 1 is for min
    :return: return the num of seen cells on the cells at the left side
    """
    is_first_col = col < 0
    if max_or_min == 0:
        if picture[row][col] == 0 or is_first_col:
            return 0
    else:
        if picture[row][col] != 1 or is_first_col:
            return 0
    return 1 + max_min_seen_left(picture, row, col - 1, max_or_min)


def max_min_seen_right(picture: list[list[int]], row: int, col: int, max_or_min: int) -> int:
    """
    :param max_or_min: 0 is for max and 1 is for min
    :return: return the num of seen cells on the cells at the right side
    """
    is_last_col = col >= len(picture[row])
    if max_or_min == 0:
        if is_last_col or picture[row][col] == 0:
            return 0
    else:
        if is_last_col or picture[row][col] != 1:
            return 0
    return 1 + max_min_seen_right(picture, row, col + 1, max_or_min)


def max_or_min_seen_cells(picture: list[list[int]], row: int, col: int, max_or_min: int) -> int:
    """
    max_or_min_seen_cells is doing the all job for max_seen_cells and min_seen_cells
    :param max_or_min: 0 is for max and 1 is for min
    :return: if max_or_min == 0 then return the max seen cells, otherwise return the min seen cells
    """
    is_row_up = row > 0
    is_row_down = (row + 1) < len(picture)
    is_col_left = col > 0
    is_col_right = (col + 1) < len(picture[row])

    counter = 1

    if is_row_up:
        counter += max_min_seen_up(picture, row - 1, col, max_or_min)

    if is_row_down:
        counter += max_min_seen_down(picture, row + 1, col, max_or_min)

    if is_col_left:
        counter += max_min_seen_left(picture, row, col - 1, max_or_min)

    if is_col_right:
        counter += max_min_seen_right(picture, row, col + 1, max_or_min)

    return counter


def max_seen_cells(picture: list[list[int]], row: int, col: int) -> int:
    if picture[row][col] == 0:
        return 0
    return max_or_min_seen_cells(picture, row, col, 0)


def min_seen_cells(picture: list[list[int]], row: int, col: int) -> int:
    if picture[row][col] != 1:
        return 0
    return max_or_min_seen_cells(picture, row, col, 1)


def check_constraints(picture: List[List[int]], constraints_set: Set[Tuple[int, int, int]]) -> int:
    is_seen_exactly = 0
    is_seen_may_exist = 0

    for const in constraints_set:
        max_cell = max_seen_cells(picture, const[0], const[1])
        min_cell = min_seen_cells(picture, const[0], const[1])
        if const[2] < min_cell or const[2] > max_cell:
            return 0
        elif max_cell >= const[2] >= min_cell:
            if min_cell == max_cell:
                is_seen_exactly += 1
            is_seen_may_exist += 1

    if is_seen_exactly == is_seen_may_exist:
        return 1
    return 2


def picture_constructor(n: int, m: int) -> list[list[int]]:
    return [[-1] * m for _ in range(n)]


def solve_puzzle_core(picture:  List[List[int]], constraints_set: set[tuple[int, int, int]],
                                            row: int, col: int, answers: list[Optional[List[List[int]]]]) -> None:

    rec_status = check_constraints(picture, constraints_set)
    if rec_status == 0:
        return

    if col == len(picture[0]):
        col = 0
        row += 1
        if row == len(picture):
            if rec_status == 1:
                answers.append(copy.deepcopy(picture))
                return

    picture[row][col] = 1
    solve_puzzle_core(picture, constraints_set, row, col + 1, answers)
    picture[row][col] = 0
    solve_puzzle_core(picture, constraints_set, row, col + 1, answers)
    picture[row][col] = -1


def solve_puzzle(constraints_set: Set[Tuple[int, int, int]], n: int, m: int) -> Optional[List[List[int]]]:
    picture = picture_constructor(n, m)
    answers: list[Optional[List[List[int]]]] = list()
    solve_puzzle_core(picture, constraints_set, 0, 0, answers)
    if len(answers) == 0:
        return None
    return answers[0]


def how_many_solutions_core(picture: list[list[int]], constraints_set: set[tuple[int, int, int]],
                                                                            row: int, col: int) -> int:
    rec_status = check_constraints(picture, constraints_set)
    counter = 0
    if rec_status == 0:
        return 0

    if col == len(picture[0]):
        col = 0
        row += 1
        if row == len(picture):
            if rec_status == 1:
                return 1

    picture[row][col] = 1
    counter += how_many_solutions_core(picture, constraints_set, row, col + 1)
    picture[row][col] = 0
    counter += how_many_solutions_core(picture, constraints_set, row, col + 1)
    picture[row][col] = -1
    return counter


def how_many_solutions(constraints_set: Set[Tuple[int, int, int]], n: int, m: int) -> int:
    picture = picture_constructor(n, m)
    return how_many_solutions_core(picture, constraints_set, 0, 0)


def generate_puzzle(picture: list[list[int]]) -> set[tuple[int, int, int]]:
    const_set = set()
    n = len(picture)
    m = len(picture[0])
    for row in range(n):
        for col in range(m):
            const_set.add((row, col, max_seen_cells(picture, row, col)))
            if how_many_solutions(const_set, n, m) == 1:
                return const_set
    return const_set
