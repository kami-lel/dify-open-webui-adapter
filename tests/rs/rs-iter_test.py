"""
rs-iter_test.py

Unit Tests (using pytest) for:

__iter__()
"""

# Pytest unit tests  ###########################################################


def test_wf(testee_wf1):
    sr, _ = testee_wf1
    opt = iter(sr)
    assert sr is opt


def test_cf(testee_cf1):
    sr, _ = testee_cf1
    opt = iter(sr)
    assert sr is opt
