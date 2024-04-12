import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.Hex_Logic import DisjointSet, Gameboard
import pytest


def test_disjoint_set_initialization():
    ds = DisjointSet(['a', 'b', 'c'])
    assert ds.parent == {'a': 'a', 'b': 'b', 'c': 'c'}
    assert ds.size == {'a': 1, 'b': 1, 'c': 1}

def test_disjoint_set_make_set():
    ds = DisjointSet([])
    ds.make_set('x')
    assert ds.parent == {'x': 'x'}
    assert ds.size == {'x': 1}

def test_disjoint_set_find():
    ds = DisjointSet(['a', 'b', 'c'])
    assert ds.find('a') == 'a'
    assert ds.find('b') == 'b'
    assert ds.find('c') == 'c'

def test_disjoint_set_union():
    ds = DisjointSet(['a', 'b', 'c'])
    ds.union('a', 'b')
    assert ds.parent == {'a': 'a', 'b': 'a', 'c': 'c'}
    assert ds.size == {'a': 2, 'b': 2, 'c': 1}

def test_gameboard_initialization():
    gb = Gameboard(5)
    assert gb.n == 5
    assert gb.board == [[0]*5 for _ in range(5)]
    assert gb.red_disjoint_set.parent == {(i, j): (i, j) for i in range(5) for j in range(5)}
    assert gb.blue_disjoint_set.parent == {(i, j): (i, j) for i in range(5) for j in range(5)}

def test_gameboard_play():
    gb = Gameboard(5)
    assert gb.play(0, 0, 'red') is None
    assert gb.play(0, 1, 'red') is None
    assert gb.play(0, 2, 'red') == 'red wins'

def test_gameboard_print_board():
    gb = Gameboard(5)
    gb.play(0, 0, 'red')
    gb.play(0, 1, 'red')
    gb.play(0, 2, 'red')
    # Capture the output of print_board and compare it to the expected output
    # This might require mocking or redirecting stdout
