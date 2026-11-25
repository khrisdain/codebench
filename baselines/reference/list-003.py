def rotate(lst, k):
    if not lst:
        return []
    k %= len(lst)
    return lst[-k:] + lst[:-k] if k else list(lst)
