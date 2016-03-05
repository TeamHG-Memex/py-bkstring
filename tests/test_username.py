from bkstring import username

def test_features():
    name = username.Username('this -.   _\n\t\vNa_me')
    assert('this' in name.dissected)
    assert('Na' in name.dissected)
    assert('me' in name.dissected)
    assert(len(name.dissected) == 3)
    assert(name.raw == 'this -.   _\n\t\vNa_me')
    assert(name.first_char == 't')
    assert(name.lower == 'this -.   _\n\t\vna_me')

def test_digits():
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

def test_no_nums():
    name = username.Username('1234')

    assert(name.no_nums == '')
