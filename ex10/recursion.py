def fib(n) :
    if n==0 :
        return 0
    elif n ==1 :
        return 1
    else :
        return fib(n-1) +fib(n-2)

# print(fib(7))

# def n_of_sums(n , k, fun):
#     if n == 0: return 1
#     elif n < 0 or k <= 0 : return 0
#     else :
#         call1 = n_of_sums(n-k, fun(k), fun)
#         call2 = n_of_sums(n, fun(k), fun)
#     return call1 + call2
#
# print(n_of_sums(6, 4, lambda a: a-1))

def subset_sum(numbers, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(numbers):
        print(i,n)
        remaining = numbers[i + 1:]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + n)

#
# print(list(subset_sum([1,5, 3, 7, 9], 10)))

# def findPairs(lst, K):
#     res = []
#     while lst:
#         num = lst.pop()
#         diff = K - num
#         if diff in lst:
#             res.append((diff, num))
#     # res.reverse()
#     return res
#
# lst = [1, 5, 3, 7, 9]
# K = 12
# print(findPairs(lst, K))

def substes_sum(lst, num):
    if num < 0:
        return
    if len(lst) == 0:
        if num == 0:
            yield []
        return
    for solution in substes_sum(lst[1:], num):
        yield solution
    for solution in substes_sum(lst[1:], num - lst[0]):
        yield [lst[0]] + solution

print(list(substes_sum([1,2,3,4,5], 5)))