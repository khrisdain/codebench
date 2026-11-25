def moving_average(lst, w):
    out = []
    i = 0
    while i + w <= len(lst):
        out.append(sum(lst[i:i + w]) / w)
    return out
