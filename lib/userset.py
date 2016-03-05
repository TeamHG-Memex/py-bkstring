from bkstring.bkgraph import BkGraph
from bkstring.bktree import BkTree
from bkstring.username import Username
from bkstring.compare import *
from bkstring.namesplitter import NameSplitter

class UserSet():
    """A set of usernames to use for suggesting similar names."""
    def __init__(self, skip_len=3, training_list=None):
        self.__skip_len = skip_len
        self.__alphas = dict()
        self.__parts = dict()
        self.__alpha_graph = BkGraph()
        self.__word_tree = BkTree()
        self.__name_splitter = self.__name_splitter(training_list)

    def add_list(self, userlist):
        # TODO: Add tuning to __name_splitter to match on large new sets of names.
        for name in userlist:
            self.__add(name)

    def __name_splitter(self, training_list):
        if training_list:
            return NameSplitter(model_filename=training_list)

        return NameSplitter()

    def add(self, username):
        # TODO:0 (C lower) Handle lowercase comparison in C library, and don't just pass it here.
        name = Username(username.lower())
        raw = name.raw

        if len(raw) > self.__skip_len:
            try:
                self.__alphas[name.alpha].append(raw)
            except KeyError:
                self.__alphas[name.alpha] = list([raw])
                self.__alpha_graph.add(name.alpha)

            for part in name.dissect(splitter=self.__name_splitter.dissect):
                # Skip parts which are too short to create a reasonable correlation.
                if len(part) <= self.__skip_len:
                    continue

                try:
                    self.__parts[part].append(raw)
                except KeyError:
                    self.__parts[part] = list([raw])
                    self.__word_tree = BkTree()


    def refine(self, query, name_part, graph, dictionary):
        """Returns all names contained in the given graph/dictionary pair which are similar to a given query."""
        # After research with a ML based matching approach for usernames, this whole implementation will be replaced with the
        # ML based approach.
        results = list()

        # Loop through each search result from the given graph:
        for part in graph.search(name_part, 1):
            for name in dictionary[part]:
                score = 0
                comp = Username(name)
                min_len = min(len(query.raw), len(comp.raw))
                overlap_min = (min_len - 1) / min_len

                # Skip over strings which are too short to get a good correlation.
                if len(comp.alpha) < self.__skip_len:
                    continue

                # Check for matching longer numbers in strings.
                if len(query.numbers) > 0 and len(comp.numbers) > 0 and overlap(query.alpha, comp.alpha, 1) > .99:
                    # Loop through the numbers in the query and comparator:
                    for num1 in query.numbers:
                        for num2 in comp.numbers:
                            # If the numbers are equal and have at least 3 digits:
                            if num1 / 100 > 1 and num1 == num2:
                                # Add to score and break.
                                score += 2
                                break
                        # Only add to score once though.
                        if score > 0:
                            break

                # Check for similar query and comparator parts, if all long parts are simlar add to score.
                # Only add to score when all the long parts are similar.
                if len(query.dissected) > 0 and len(comp.dissected) > 0:
                    potential = False
                    for word1 in query.dissected:
                        if len(word1) < self.__skip_len:
                            continue

                        for word2 in comp.dissected:
                            if len(word2) < self.__skip_len:
                                continue

                            if overlap(word1, word2, 2) > overlap_min:
                                potential = True

                            else:
                                potential = False
                                break

                        if not potential:
                            break

                    # Only add to score if all long parts are matched for
                    if potential:
                        score += 1

                # If the query and comparator without numbers are equal:
                if query.no_nums == comp.no_nums:
                    score += 1

                # If the query and comparator without spaces or punctuation are equal:
                if query.no_punc == comp.no_punc:
                    score += 1

                # If the first part of the query and comparator split by numbers are equal:
                if query.split_nums[0] == comp.split_nums[0] and len(query.split_nums[0]) > 2:
                    score += 1

                # If there is a high overlap of bigrams between the query and comparator:
                if overlap(query.alpha, comp.alpha, 2) > overlap_min:
                    score += 1

                # If the beginning of the query and comparator are equal and the overlap of bigrams are relatively high:
                if query.raw[:3] == comp.raw[:3] and overlap(query.raw, comp.raw, 2) > .9:
                    score += 1

                # Only add names to results if they have a high enough score.
                if score > 4:
                    results.append(comp.raw)

        return results

    def search(self, username, max_results=10):
        """
        Returns a list of suggested similar usernames based on the set contained in this UserSet.

        Defaults:
        max_results = 10 (If there are more than 10 results, there is a likelihood the results are too messy.)
        """

        # TODO:10 (C lower) Handle lowercase comparison in C library, and don't just pass it here.
        query_name = Username(username.lower())
        query_raw = query_name.raw

        if len(query_raw) < self.__skip_len:
            return

        results = list()
        for part in query_name.dissect(self.__name_splitter.dissect):
            if len(part) <= self.__skip_len:
                continue

            # Search the word BK Tree for similar usernames
            results.extend(self.refine(query_name, part, self.__word_tree, self.__parts))
            # Search the alphabet BK Tree graph for similar usernames
            results.extend(self.refine(query_name, part, self.__alpha_graph, self.__alphas))

        results = list(set(results))

        if len(results) < max_results:
            return results

    def close(self):
        """
        Close the UserSet.
        """
        self.__alpha_graph.close()
        self.__word_tree.close()
