def most_common_char(s):
    counts = {}
    for c in s:
        if c != ' ':
            counts[c] = counts.get(c, 0) + 1
    return max(counts, key=counts.get)
