import pytest
from interrobench.main import has_n_duplicates, most_common_element, EqualCountError

def test_has_n_duplicates():
    # Test cases where there are at least n True values
    assert has_n_duplicates(2, [True, True, False]) is True
    assert has_n_duplicates(3, [True, True, True]) is True

    # Test cases where there are at least n False values
    assert has_n_duplicates(2, [True, False, False]) is True
    assert has_n_duplicates(3, [False, False, False]) is True

    # Test cases where n is not satisfied
    assert has_n_duplicates(4, [True, True, False, False]) is False
    assert has_n_duplicates(1, []) is False  # Edge case: empty list

def test_most_common_element():
    # Test cases where True is more common
    assert most_common_element([True, True, False]) is True
    assert most_common_element([True, True, True]) is True

    # Test cases where False is more common
    assert most_common_element([False, False, True]) is False
    assert most_common_element([False, False, False]) is False

    # Test cases where True and False occur equally
    with pytest.raises(EqualCountError):
        most_common_element([True, False])
    with pytest.raises(EqualCountError):
        most_common_element([])  # Edge case: empty list
