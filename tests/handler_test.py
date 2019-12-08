import pytest

from handler import find_diffs


def test_find_diffs_no_change():
    prev = {
        'loc1': 'closed',
        'loc2': 'open',
        'loc3': 'conditions variable'
    }
    curr = prev.copy()

    diffs = find_diffs(prev, curr)
    assert len(diffs) == 0

def test_find_diffs_with_change():
    prev = {
        'loc1': 'closed',
        'loc2': 'open',
        'loc3': 'conditions variable'
    }
    curr = {
        'loc1': 'open',
        'loc2': 'open',
        'loc3': 'conditions variable'
    }

    diffs = find_diffs(prev, curr)
    
    assert len(diffs) == 1

    location, prev_status, curr_status = diffs[0]
    assert location == 'loc1'
    assert prev_status == 'closed'
    assert curr_status == 'open'

def test_find_diffs_multiple_changes():
    prev = {
        'loc1': 'closed',
        'loc2': 'open',
        'loc3': 'conditions variable'
    }
    curr = {
        'loc1': 'open',
        'loc2': 'closed',
        'loc3': 'open'
    }

    diffs = find_diffs(prev, curr)

    assert len(diffs) == 3

    l, p, c = diffs[0]
    assert l == 'loc1'
    assert p == 'closed'
    assert c == 'open'

    l, p, c = diffs[1]
    assert l == 'loc2'
    assert p == 'open'
    assert c == 'closed'

    l, p, c = diffs[2]
    assert l == 'loc3'
    assert p == 'conditions variable'
    assert c == 'open'

