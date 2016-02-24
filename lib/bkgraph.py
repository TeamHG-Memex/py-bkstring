from lib import bkstring

class BkGraph():
    def __init__(self, fn='l_dist'):
        self.fn = fn
        self.trees = dict()

    def add(self, word):
        length = len(word)

        try:
            self.trees[length].add(word)
        except KeyError:
            self.trees[length] = bkstring.BkTree(self.fn)
            self.trees[length].add(word)

    def add_list(self, arr):
        for word in arr:
            self.add(word)

    def search(self, word, dist=0):
        results = list()

        for idx, key in enumerate(self.trees):
            diff = self._get_diff(word, key, dist)
            results.extend(self.trees[key].search(word, diff))

        return list(set(results))

    def close(self):
        for idx, key in enumerate(self.trees):
            self.trees[key].close()

    def _get_diff(self, word, key, dist):
        length = len(word)

        if self.fn == 'l_dist':
            return max(length - key, key - length) + dist

        if self.fn == 'mod_j_dist':
            first = max(length, key)
            second = min(length, key)

            return min(100 - int(100 * (second - dist) / (first + dist)), 100)
