from bkstring import bkgraph

def test_ldist_bkgraph():
    graph = bkgraph.BkGraph()

    graph.add('foo')

    ls = graph.search('foo', 1)

    assert('foo' in ls)

    arr = list(['bar', 'baz'])
    graph.add_list(arr)

    ls = graph.search('bar', 1)

    assert('baz' in ls)

    graph.close()

def test_jdist_bkgraph():
    graph = bkgraph.BkGraph(fn='mod_j_dist')

    graph.add('foo')
    graph.add('food')
    graph.add('bar')

    ls = graph.search('btar', 0)

    assert('bar' in ls)

    graph.close()
