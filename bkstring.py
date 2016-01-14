"""
A Python wrapper for bkstring C library.

Find the bkstring project at:
https://github.com/bcmackintosh/bk-string

Usage:

# Import the library, currently expects the "libbkstring.so" to be at
# "./deps/libbkstring.so" and "bkstring.py" to be at "./bkstring.py."
import bkstring

# Initialize
b = bkstring.bk_tree()

# Add words
b.add("foo")

# Add a list of words
arr = list("foo", "bar")
b.add_list(arr)

# Search
ls = b.search("foo", 1)
assert()

# Close the BK tree
b.close()

If you fail to close the BK Tree the module will segfault after execution.
"""
# TODO: Create a Setup.py with:
#       Export of this module
#       Handling the "libbkstring.so" shared library

from ctypes import *
from itertools import takewhile

class BKNODE(Structure):
    pass
BKNODE._fields_ = [("word", c_wchar_p),
    ("child", POINTER(BKNODE)),
    ("empty", c_uint64),
    ("size", c_uint64)]

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
    _free_list = bkstring.free_list

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
        ls = cast(self._search(
                c_char_p(word),
                c_uint64(dist),
                byref(self.tree)),
            POINTER(c_char_p))

        iter_ls = takewhile(lambda x: x is not None, ls)

        arr = list()

        for i in iter_ls:
            arr.append(i)

        # Get rid of the crazy ctypes pointer list, so we return a reasonable python one.
        self._free_list(ls)

        return arr

    def close(self):
        self._clear_bktree(self.tree)
