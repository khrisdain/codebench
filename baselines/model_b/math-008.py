def sum_of_multiples(limit):
    return sum(i for i in range(limit + 1) if i % 3 == 0 or i % 5 == 0)
