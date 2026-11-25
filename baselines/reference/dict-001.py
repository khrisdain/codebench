def word_frequencies(text):
    counts = {}
    for word in text.lower().split():
        word = word.strip('.,!?')
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts
