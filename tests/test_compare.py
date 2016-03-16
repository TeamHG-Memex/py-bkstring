from bkstring.compare import *

def test_overlap():
    assert overlap('foo', 'food') == 1
    assert overlap('joe', 'bar') < 1

def test_jaccard():
    assert j_dist('foo', 'food') == 3/4
