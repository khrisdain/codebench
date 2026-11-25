def moving_average(lst, w):
    return [sum(lst[i:i + w]) / w for i in range(len(lst) - w + 1)]
