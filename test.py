"""
Hacky test file for bkstring.py
"""
# TODO: Create a real test suite for the py-bkstring.

import bkstring

b = bkstring.bk_tree()

b.add("foo")

ls = b.search("foo", 1)

assert(ls[0] == "foo")

arr = list(["bar", "baz"])
b.add_list(arr)

ls = b.search("bar", 1)

assert(len(ls) == 2)

b.close()
