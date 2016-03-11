from bkstring.bktree import BkTree

class BkGraph():
    def __init__(self, fn='l_dist'):
        self.fn = fn
        self.trees = dict()

        if fn == 'hex_ham_dist':
            # TODO: Implement hex_ham_dist into BkGraph, needs a way to measure 'len()'
            raise NotImplementedError('\'hex_ham_dist\' has not been implemented in Bk Graph.')

    def add(self, word):
        length = len(word)

        try:
            self.trees[length].add(word)
        except KeyError:
            self.trees[length] = BkTree(self.fn)
            self.trees[length].add(word)

    def add_list(self, arr):
        for word in arr:
            self.add(word)

    def search(self, word, dist, variance=None):
        results = list()
        length = len(word)

        for idx, key in enumerate(self.trees):
            if variance is not None and length - variance > length - abs(key - length):
                # If the variance from this key is less than the allowable variance, skip this word.
                continue
            if variance is not None and length + variance < length + abs(key - length):
                # If the variance from this key is greater than the allowable variance, skip this word.
                continue

            diff = self.__get_diff(word, key, dist)
            results.extend(self.trees[key].search(word, diff))

        return list(set(results))

    def close(self):
        for idx, key in enumerate(self.trees):
            self.trees[key].close()

    def __get_diff(self, word, key, dist):
        length = len(word)

        if self.fn == 'l_dist':
            return max(length - key, key - length) + dist

        if self.fn == 'mod_j_dist':
            first = max(length, key)
            second = min(length, key)

            return min(100 - int(100 * (second - dist) / (first + dist)), 100)

        return dist
