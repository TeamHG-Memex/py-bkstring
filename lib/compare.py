def get_ngrams(word, n):
    word = str(word)
    return [word[i:i + n] for i in range(0, len(word) - n + 1)]

def overlap(first, second, ngram_size=1):
    fir = get_ngrams(first, ngram_size)
    sec = get_ngrams(second, ngram_size)

    den = min(len(fir), len(sec))

    if den <= 0:
        return overlap(first, second, ngram_size - 1)
    count = 0

    for i in range(0, len(fir)):
        for j in range(0, len(sec)):
            if fir[i] == sec[j]:
                count += 1
                sec = sec[:j] + sec[j + 1:]
                break

    return (count / float(den))

def dist(first, second):
    return (overlap(first, second, 3) * 5
        + overlap(first, second, 2) * 35
        + overlap(first, second, 1) * 60) / 100

def longest_string(first, second):
    count = 0
    keep = 0
    for i in range(0, len(first)):
        for j in range(0, len(second)):
            if first[i] == second[j]:
                count += 1
            else:
                if count > keep:
                    keep = count
                count = 0
                break

    return keep
