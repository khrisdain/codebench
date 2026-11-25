def is_anagram(a, b):
    norm = lambda x: sorted(x.replace(' ', '').lower())
    return norm(a) == norm(b)
