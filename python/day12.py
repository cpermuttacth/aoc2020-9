from collections import deque

manhattan = lambda n: abs(n.real) + abs(n.imag)
last = lambda L: deque(L, maxlen=1).pop()

def navigate(L, p=0+0j, v=1+0j, m=1):
    for cmd, n in [(x[0], int(x[1:])) for x in L]:
        if   m==1 and cmd == 'N': p += n * (+0-1j)
        elif m==1 and cmd == 'E': p += n * (+1+0j)
        elif m==1 and cmd == 'S': p += n * (+0+1j)
        elif m==1 and cmd == 'W': p += n * (-1+0j)
        elif m==2 and cmd == 'N': v += n * (+0-1j)
        elif m==2 and cmd == 'E': v += n * (+1+0j)
        elif m==2 and cmd == 'S': v += n * (+0+1j)
        elif m==2 and cmd == 'W': v += n * (-1+0j)
        elif cmd == 'F': p += n * v
        elif cmd == 'R': v *= [1, 1j, -1, -1j][n//90]
        elif cmd == 'L': v *= [1, -1j, -1, 1j][n//90]
        else: raise Exception(f"WTF? {cmd}{n}")
        yield p, v

def day12a(lines): return manhattan(last(navigate(lines))[0])
def day12b(lines): return manhattan(last(navigate(lines, v=10-1j, m=2))[0])

def test_12_ex1a(): assert [*navigate(ex1)] == [(10+0j, 1+0j), (10-3j, 1+0j), (17-3j, 1+0j), (17-3j, 0+1j), (17+8j, 0+1j)]
def test_12_ex1b(): assert day12a(ex1) == 25

def test_12_ex2a(): assert [*navigate(ex1, v=10-1j, m=2)] == [(100-10j, 10-1j), (100-10j, 10-4j), (170-38j, 10-4j), (170-38j, 4+10j), (214+72j, 4+10j)]
def test_12_ex2b(): assert day12b(ex1) == 286

def test_12a(day12_lines): assert day12a(day12_lines) == 938
def test_12b(day12_lines): assert day12b(day12_lines) == 54404

def test_12_learn_math():
    # an "R270" instruction means three consecutive 90° rotations right. Starting with "1 north, 10 east"...
    assert (10-1j) * 1j == (1+10j) # 10 south, 1 east
    assert (1+10j) * 1j == (-10+1j) # 1 north, 10 west
    assert (-10+1j) * 1j == (-1-10j) # 10 north, 1 west

    # but can't do three rotations like this (* 3 * 1j) --
    assert (10-1j) * (3 * 1j) == (3+30j)
    assert (10-1j) * 1j * 1j * 1j == (-1-10j)
    assert (10-1j) * (0-1j) == (-1-10j)

    # solution: https://docs.python.org/3/library/cmath.html#cmath.rect
    import math, cmath
    assert cmath.isclose((10-1j) * cmath.rect(1, math.radians(270)), (-1-10j))
    # or with math.cos and math.sin...
    assert cmath.isclose((10-1j) * (math.cos(math.radians(270)) + math.sin(math.radians(270)) * 1j), (-1-10j))
    # but this suffers from floating point inaccuracy, so have to use cmath.isclose here.

ex1 = 'F10|N3|F7|R90|F11'.split('|')
