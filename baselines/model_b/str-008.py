def caesar_shift(s, k):
    return ''.join(chr(ord(c) + k) if c.isalpha() else c for c in s)
