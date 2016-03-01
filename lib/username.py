import re

class Username():
    def __init__(self, username):
        self.raw = username
        self.dissected = self.__dissect()
        self.first_char = self.__first_char()
        self.lower = self.__lower()
        self.numbers = self.__numbers()
        self.words = self.__words()
        self.no_nums = self.__no_nums()
        self.no_punc = self.__no_punc()
        self.alpha = self.__alpha()
        self.has_punc = self.__has_punc()
        self.has_space = self.__has_space()
        self.split_nums = self.__split_nums()
        # self.initials = self.__initials()

    def __dissect(self):
        """
        Returns a list of strings based on the username being split
        by whitespace, '.', '-', and '_'
        """
        return re.split('[\s\t\n\v\-._\d]+', self.raw)

    def __first_char(self):
        """Returns the first letter of the username."""
        return self.raw[:1]

    def __lower(self):
        """Returns an all lowercase version for the username."""
        return self.raw.lower()

    def __numbers(self):
        """Placeholder Function"""
        ret = list()
        arr = re.findall('\d+', self.raw)

        for num in arr:
            ret.append(int(num))

        return ret

    def __words(self):
        """Placeholder Function"""
        return None

    def __no_nums(self):
        return re.sub('\d+', '', self.raw)

    def __no_punc(self):
        return re.sub('[,.\-_@\s]+', '', self.raw)

    def __alpha(self):
        return re.sub('[,.\-_@\d\s]+', '', self.raw)

    def __has_punc(self):
        return re.match('[,.\-_]+', self.raw)

    def __has_space(self):
        return re.match('[\s]+', self.raw)

    def __split_nums(self):
        return re.split('[\d]+', self.raw)

    # def __initials(self):
    #     initials = ''
    #     for w in self.dissected:
    #         initials += w[0]
    #
    #     return initials
