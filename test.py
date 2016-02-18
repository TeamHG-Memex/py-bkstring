"""
Hacky test file for bkstring.py
"""
# TODO: Create a real test suite for the py-bkstring.

from bkstring import bkstring
from bkstring import bkgraph

print "testing bk tree"

b = bkstring.bk_tree()

b.add("foo")

ls = b.search("foo", 1)

assert(ls[0] == "foo")

arr = list(["bar", "baz"])
b.add_list(arr)

ls = b.search("bar", 1)

assert(len(ls) == 2)

print "tests OK!"

print "testing bk graph"

b.close()

graph = bkgraph.BkGraph()

graph.add("foo")

ls = graph.search("foo", 1)

assert("foo" in ls)

arr = list(["bar", "baz"])
graph.add_list(arr)

ls = graph.search("bar", 1)

assert("baz" in ls)

print "tests OK!"
