import ex7_helper
from typing import *


def mult(x: float, y: int) -> float:
    if y == 0:
        return 0
    sub_y = ex7_helper.subtract_1(y)
    rec_sum = mult(x, sub_y)
    return float(ex7_helper.add(x, rec_sum))


def is_even(n: int) -> bool:
    if n == 0:
        return True
    prev_n = ex7_helper.subtract_1(n)
    return not is_even(prev_n)


def log_mult(x: float, y: int) -> float:
    if y == 0:
        return 0
    elif y == 1:
        return x
    n = log_mult(x, ex7_helper.divide_by_2(y))
    if not (ex7_helper.is_odd(y)):
        return ex7_helper.add(n, n)
    else:
        n = ex7_helper.add(n, n)
        return ex7_helper.add(n, x)


def is_power_core(pow_b: float, b: int, x: int) -> bool:
    if b == x or pow_b == x:
        return True
    elif b > x or pow_b > x:
        return False
    else:
        pow_b = log_mult(pow_b, b)
        return is_power_core(pow_b, b, x)


def is_power(b: int, x: int) -> bool:
    if (b == 1 and x != 1) or (b == 0 and (x != 1 or x != 0)):
        return False
    elif b != 1 and x == 1:
        return True
    return is_power_core(b, b, x)


def reverse_core(s: str, n: int, len_s: int) -> str:
    """
    from Ex7 forum:

        Dvir Sasson (question):
            "במימוש הפונקציה reverse:
                מותר להשתמש בפונקציות add, substract 1 וכו?"

            Idan Refaeli (answer):
                 "אפשר (ובשאלה זו אפשר גם להשתמש באופרטור + לחיבור בין מספרים ישירות)"
    """
    if n == len_s:
        return ""
    next_n = n + 1
    rev_s = reverse_core(s, next_n, len_s)
    return ex7_helper.append_to_end(rev_s, s[n])


def reverse(s: str) -> str:
    return reverse_core(s, 0, len(s))


def play_hanoi(hanoi: Any, n: int, src: Any, dst: Any, temp: Any) -> Any:
    if n <= 0:
        return

    play_hanoi(hanoi, n - 1, src, temp, dst)
    hanoi.move(src, dst)
    play_hanoi(hanoi, n - 1, temp, dst, src)


def count_one_in_n(n: int) -> int:
    counter = 0

    n_mod_10 = n % 10
    n_dev_10 = n // 10

    if n_mod_10 == 1 and n_dev_10 == 1:
        counter += 2
    elif n_mod_10 == 1 or n_dev_10 == 1:
        counter += 1

    return counter


def number_of_ones(n: int) -> int:
    if n <= 0:
        return 0

    n_dev_f_10 = n // 10

    counter = count_one_in_n(n)

    if n_dev_f_10 > 9:
        counter += count_one_in_n(n_dev_f_10)

    return counter + number_of_ones(n - 1)


def compare_2d_lists_core(l1: list[list[int]], l2: list[list[int]], n1: int, n2: int) -> bool:
    if n2 == -1 and n1 != -1:
        n1 -= 1
        return True and compare_2d_lists_core(l1, l2, n1, len(l1[n1]) - 1)

    if n1 == -1:
        return True

    l_of_l1 = l1[n1]
    l_of_l2 = l2[n1]

    if len(l_of_l1) != len(l_of_l2):
        return False

    cord_1 = l_of_l1[n2]
    cord_2 = l_of_l2[n2]

    if cord_1 != cord_2:
        return False

    return True and compare_2d_lists_core(l1, l2, n1, n2 - 1)


def compare_2d_lists(l1: list[list[int]], l2: list[list[int]]) -> bool:
    if len(l1) != len(l2):
        return False

    if len(l1) == 0:
        return True

    n1 = len(l1) - 1
    n2 = len(l1[n1]) - 1

    return compare_2d_lists_core(l1, l2, n1, n2)


def plus_lists(lst1: list[Any], lst2: list[Any], n: int) -> list[Any]:
    if n == len(lst2):
        return lst1
    lst1.append(lst2[n])
    return plus_lists(lst1, lst2, n + 1)


def magic_list(n: int) -> List[Any]:
    if n == 0:
        return []

    cord = [magic_list(n - 1)]
    lst = magic_list(n - 1)

    lst = plus_lists(lst, cord, 0)
    return lst

