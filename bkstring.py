"""
A Python wrapper for bkstring C library.

Find the bkstring project at:
https://github.com/bcmackintosh/bk-string

Usage:

# Import the library, currently expects the "libbkstring.so"
import bkstring

# Initialize
b = bkstring.bk_tree()

# Add words
b.add("foo")

# Add a list of words
ls = list("foo", "bar")
b.add_list(ls)

# Search
ls = b.search

# Close the BK tree
b.close()
"""
# TODO: Create a Setup.py with:
#       Export of this module
#       Handling the "libbkstring.so" shared library

from ctypes import *
from itertools import takewhile

class BKNODE(Structure):
    pass
class BKNODE(Structure):
    BKNODE._fields_ = [("word", c_wchar_p),
    ("child", POINTER(BKNODE)),
    ("empty", c_int),
    ("size", c_int)]

class BKTREE(Structure):
    _fields_ = [("_root", BKNODE)]

class bk_tree(object):
    # Import the BK String shared library
    bkstring = CDLL("./deps/libbkstring.so")

    _bk_add = bkstring.bk_add
    _search = bkstring.search
    _clear_bktree = bkstring.clear_bktree
    _init = bkstring.init
    _close = bkstring.close

    def __init__(self):
        self.tree = BKTREE(BKNODE())
        self._init(byref(self.tree))

    def add(self, word):
        self._bk_add(c_char_p(word), byref(self.tree))

    def add_list(self, ls):
        for i in ls:
            self.add(i)

    def search(self, word, dist):
        # TODO: See if there's a less hacky way to handle the uint8_t** returned from "_search()"
        ls = takewhile(lambda x: x is not None, cast(self._search(c_char_p(word), c_uint64(dist), byref(self.tree)), POINTER(c_char_p)))
        ret = list()

        for i in ls:
            ret.append(i)

        return ret

    def close(self):
        # TODO: Actually make "_clear_bktree()" work as expected.  Not a huge deal because exiting bkstring should free memory allocations,
        # but, still worth looking into.

        # self._clear_bktree(self.tree)
        self._close()
