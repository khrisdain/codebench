def word_frequencies(text):
    counts = {}
    for word in text.split():
        word = word.strip('.,!?')
        counts[word] = counts.get(word, 0) + 1
    return counts
