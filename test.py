'''
Hacky test file for bkstring.py
'''
# TODO: Create a real test suite for the py-bkstring.

from bkstring import bkstring
from bkstring import bkgraph

print('testing bk tree')

b = bkstring.BkTree()

# b.add('foo')
#
# ls = b.search('foo', 1)
#
#
# assert(ls[0] == b'foo')
#
# ls = b.search('bar', 1)
#
# assert(len(ls) == 0)

# arr = list(['bar', 'baz'])
# b.add_list(arr)

b.add('bar')
b.add('baz')

ls = b.search('bar', 1)

# assert(len(ls) == 2)
assert('baz' in ls)
assert('bar' in ls)

b.close()

b = bkstring.BkTree(fn='mod_j_dist')

b.add('foo')

ls = b.search('fo', 34)

assert(ls[0] == 'foo')

b.close()

print('tests OK!')

print('testing bk graph')

graph = bkgraph.BkGraph()

graph.add('foo')

ls = graph.search('foo', 1)

assert('foo' in ls)

arr = list(['bar', 'baz'])
graph.add_list(arr)

ls = graph.search('bar', 1)

assert('baz' in ls)

graph.close()

print('tests OK!')

print('Testing the modified Jaccard Distance on BK Tree')
b = bkstring.BkTree(fn='mod_j_dist')

b.add('foo')
b.add('food')

ls = b.search('foo', 25)

assert('foo' in ls)
assert('food' in ls)

ls = b.search('foo', 10)
assert('foo' in ls)
assert('food' not in ls)

b.close()

print('tests OK!')

print('Testing the modified Jaccard Distance on BK Graph')

graph = bkgraph.BkGraph(fn='mod_j_dist')

graph.add('foo')
graph.add('food')
graph.add('bar')

ls = graph.search('btar')

assert('bar' in ls)

graph.close()

print('tests OK!')
