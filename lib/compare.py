from ctypes import *
import os

dll_loc = os.path.join(os.path.dirname(__file__), 'shared/libbkstring.so')
bkstring = CDLL(dll_loc)
_jaro_dist = bkstring.jaro_dist

MAX_PERCENT_DIST = 100

def convert_word(word):
    return c_char_p(word.encode('utf-8'))

def jaro_dist(word1, word2):
    return _jaro_dist(convert_word(word1), convert_word(word2))

def prefix_match(word1, word2):
    matches = 0
    for i in range(min(4, min(len(word1), len(word2)))):
        if word1[i] == word2[i]:
            matches += 1

    return matches

def jaro_wink_sim(word1, word2, weight=.1):
    jaro = (100 - jaro_dist(word1, word2)) / 100
    p = prefix_match(word1, word2)
    return jaro + (weight * p * (1 - jaro))

def get_ngrams(word, n):
    word = str(word)
    return [word[i:i + n] for i in range(0, len(word) - n + 1)]

def overlap(first, second, ngram_size=1):
    fir = get_ngrams(first, ngram_size)
    sec = get_ngrams(second, ngram_size)

    den = min(len(fir), len(sec))

    if den <= 0:
        return 0

    count = 0

    for i in range(0, len(fir)):
        for j in range(0, len(sec)):
            if fir[i] == sec[j]:
                count += 1
                sec = sec[:j] + sec[j + 1:]
                break

    return (count / float(den))

def j_dist(first, second, ngram_size=1):
    fir = get_ngrams(first, ngram_size)
    sec = get_ngrams(second, ngram_size)

    if min(len(fir), len(sec)) <= 0 :
        return 1

    den = len(fir) + len(sec)
    num = 0

    for i in range(0, len(fir)):
        for j in range(0, len(sec)):
            if fir[i] == sec[j]:
                num += 1
                den -= 1
                sec = sec[:j] + sec[j + 1:]
                break

    return (num / float(den))

def l_dist(first, second, ngram_size=1):
    fir = get_ngrams(first, ngram_size)
    sec = get_ngrams(second, ngram_size)

    if len(fir) == 0:
        return len(sec)
    if len(sec) == 0:
        return len(fir)

    dist = [[i for i in range(len(sec) + 1)] for j in range(len(fir) + 1)]

    for i in range(1, len(fir)):
        for j in range(1, len(sec)):
            match = 1

            if fir[i] == sec[j]:
                match = 0

            dist[i][j] = min(min(dist[i][j - 1] + 1, dist[i - 1][j] + 1), dist[i - 1][j - 1] + match)

    return dist[len(fir)][len(sec)]

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
