# 2021b-5
def n_of_sums(n, k, fun):
    """
    :param n: positive int number
    :param k: positive int number
    :param fun: function with positive arg
    :return: different number of times that we can sum the decreasing seq to be equal to number n
    """

    # find the seq
    # count different sum

    lst = list(k)
    while k > 1:
        k = fun(k)
        lst.append(k)


#2021a-combination lock

def combination_lock(*args):
    """
    :param args: int numbers
    :return: function which returns bool val
    """
    # return a func
    # return bool
    return helper(args, 0, True)


def helper(lst, ind, bol):
    def g(arg):
        if ind == len(lst)-1:
            return bol and lst[ind] == arg
        return helper(lst, ind + 1, bol and lst[ind] == arg)
        # if lst[ind] == arg :
        #     return helper(lst, ind+1, bol and True)
        # if lst[ind] != arg:
        #     return helper(lst, ind+1, bol and False)
    return g


f = combination_lock(1,2,3,4)
print(f(1)(2)(3)(4))
























