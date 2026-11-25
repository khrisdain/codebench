def run_length_encode(s):
    out = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            out.append(f'{s[i - 1]}{count}')
            count = 1
    return ''.join(out)
