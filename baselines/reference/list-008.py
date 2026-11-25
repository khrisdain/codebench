def max_subarray_sum(lst):
    best = cur = lst[0]
    for x in lst[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
