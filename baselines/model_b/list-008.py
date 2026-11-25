def max_subarray_sum(lst):
    best = cur = 0
    for x in lst:
        cur = max(0, cur + x)
        best = max(best, cur)
    return best
