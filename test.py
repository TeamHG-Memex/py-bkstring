'''
Hacky test file for Py-BkString
'''
# TODO:20 Create a real test suite for the py-bkstring.

from bkstring import bktree
from bkstring import bkgraph
from bkstring import username

print('testing bk tree')

b = bktree.BkTree()

b.add('foo')

ls = b.search('foo', 1)

assert(ls[0] == 'foo')

ls = b.search('bar', 1)

assert(len(ls) == 0)

arr = list(['bar', 'baz'])
b.add_list(arr)

b.add('bar')
b.add('baz')

ls = b.search('bar', 1)

assert(len(ls) == 2)
assert('baz' in ls)
assert('bar' in ls)

b.close()

b = bktree.BkTree(fn='mod_j_dist')

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
b = bktree.BkTree(fn='mod_j_dist')

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

print('Testing usernames dissect')

# General test for the regex to make sure it's matching as expected.
name = username.Username('this -.   _\n\t\vNa_me')
assert('this' in name.dissected)
assert('Na' in name.dissected)
assert('me' in name.dissected)
assert(len(name.dissected) == 3)
assert(name.raw == 'this -.   _\n\t\vNa_me')
assert(name.first_char == 't')
assert(name.lower == 'this -.   _\n\t\vna_me')

print('tests OK!')

print('Testing digit finding')

name = username.Username('joe1234')

assert(1234 in name.numbers)

name = username.Username('j1o2e3b4l5o6w7')

assert(1 in name.numbers)
assert(2 in name.numbers)
assert(3 in name.numbers)
assert(4 in name.numbers)
assert(5 in name.numbers)
assert(6 in name.numbers)
assert(7 in name.numbers)

name = username.Username('1234')

assert(name.no_nums == '')

print('tests OK!')
