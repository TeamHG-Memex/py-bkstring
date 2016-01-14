from sys import argv

import bkstring
import time

def benchmark(filename, word, dist):
    b = bkstring.bk_tree()
    print "begin!"

    arr = list()

    with open(filename, 'r') as f:
        for line in f:
            arr.append(line.strip())

    start = time.time()
    build_start = time.time()
    b.add_list(arr)
    build_end = time.time()

    search_start = time.time()
    ls = b.search(word, int(dist))
    search_end = time.time()
    end = time.time()

    results = ''
    for i in ls:
        results = results + str(i) + ', '

    results = results[:-2]
    print results

    print "build time: ", int((build_end - build_start) * 1000), "ms"
    print "search time: ", int((search_end - search_start) * 1000), "ms"
    print "total time: ", int((end - start) * 1000), "ms"

    b.close()

if __name__ == "__main__":
    if (len(argv) < 4):
        print "Expected 3 arguments to be given\n\nExample:\n     \"$ python bench.py <filename> <string> <distance>\""
        exit()

    filename = argv[1]
    word = argv[2]
    dist = argv[3]

    benchmark(filename, word, dist)
