# Py-BKString
A python wrapper for the BK String C project.

That project can be found at:
https://github.com/bcmackintosh/bk-string

# BK Tree Usage

## Code Example
```python
# Create a BK Tree
from bkstring.bktree import BkTree

# By Default this uses Levenshtein Distance to map strings into the tree
b = BkTree()

# Add strings

b.add('foo')

# Add a list of words

b.add_list(['foo', 'bar'])

# Search

ls = b.search('foo', 1)
assert('foo' in ls)

# Close the BK tree

b.close()
```

## Using other distance functions
Unfortunately for the time being, distance functions are limited to those implemented in the C library.  

### Implemented distance functions
* Levenshtein Distance: Edit distance based on replacements, deletions and insertions
* Modified Jaccard Distance: This matches character intersection and union sets based on the character, and number of times it occurs.  For example, the modified union of "johndoe" and "jdoe" would be "johndoe," while the unmodified union would be "johnde."

*Coming Soon: A hash hamming distance function for hex strings.*

### Setting the distance function on the BK Tree

```python
# Levenshtein Distance (default)
b = BkTree(fn='l_dist')

# Modified Jaccard Distance
b = BkTree(fn='mod_j_dist')
```
*If "fn" is set to any other string, it will default to Levenshtein Distance.*

# BK Graph Usage
A "BK Graph" is a made up structure which dynamically sets distances based on string lengths, so that the difference in string lengths are ignored.  An example would be, "johndoe" and "jdoe" have edit distance 0, while "johndoe" and "jdoa" have edit distance 1.

## Code Example
BK Graph is almost identical usage as the BK Tree class, with a couple extra capabilities.

```python
# Create the BK Graph
from bkstring.bkgraph import BkGraph()

# This defaults to using Levenshtein Distance as the distance function.
g = BkGraph()

# Create a BK Graph with a different distance function

g = BkGraph(fn='mod_j_dist')
g = BkGraph(fn='l_dist')

# Add strings
g.add('foo')

# Add a list of strings
g.add_list(['foo', 'bar', 'baz'])

# Search for strings
ls = g.search('food', 0)

assert('foo' in ls)

# Shut it down
g.close()
```

## Variance
Since the BK Graph uses a dynamic distance based on string length difference, we can also set what we want our variance of string length difference to be.  For example if we have:

    g.add_list(['foo', 'bar', 'barkingmadcat'])

We may want to search for strings matching the query string's length, but having a large edit distance.  For instance:

```python
ls = g.search('foo', 3, variance=0)
ls == ['foo', 'bar']
```

Similarly we may want to search for only strings which have 0 edit distance, but may be longer or shorter:

```python
ls = g.search('bar', 0, variance=3)
ls == ['bar']
```

By default variance is `None`, which allows the `BkGraph` to search for any length difference using the dynamic edit distance.
