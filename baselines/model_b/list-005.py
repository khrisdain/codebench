def second_largest(lst):
    distinct = sorted(set(lst))
    return distinct[-2] if len(distinct) >= 2 else None
