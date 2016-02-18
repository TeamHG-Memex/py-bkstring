import bkstring

class BkGraph():
    def __init__(self):
        self.trees = dict()

    def add(self, word):
        length = len(word)

        try:
            self.trees[length].add(word)
        except KeyError:
            self.trees[length] = bkstring.bk_tree()
            self.trees[length].add(word)

    def add_list(self, arr):
        for word in arr:
            self.add(word)

    def search(self, word, dist):
        results = list()

        for idx, key in enumerate(self.trees):
            diff = (max(len(word) - key, key - len(word)) + dist)
            results.extend(self.trees[key].search(word, diff))

        return list(set(results))

    def close(self):
        for idx, key in enumerate(self.trees):
            self.trees[key].close()
