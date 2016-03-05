from bkstring import bktree

def test_ldist_bktree():
    b = bktree.BkTree()

    b.add('foo')

    ls = b.search('foo', 1)

    assert ls[0] == 'foo'

    ls = b.search('bar', 1)

    assert len(ls) == 0

    arr = list(['bar', 'baz'])
    b.add_list(arr)

    b.add('bar')
    b.add('baz')

    ls = b.search('bar', 1)

    assert len(ls) == 2
    assert 'baz' in ls
    assert 'bar' in ls

    b.close()

def test_jdist_bktree():
    b = bktree.BkTree(fn='mod_j_dist')

    b.add('foo')

    ls = b.search('fo', 34)

    assert 'foo' in ls
    assert 'fo' not in ls

    b.add('food')

    ls = b.search('foo', 25)

    assert 'foo' in ls
    assert 'food' in ls

    ls = b.search('foo', 10)

    assert 'foo' in ls
    assert 'food' not in ls

    b.close()
