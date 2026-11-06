import pytest
from finance import calculate_total

def test_calculate_total():
    data = [{"category": "A", "amount": 100}, {"category": "B", "amount": 200}]
    assert calculate_total(data) == 300

def test_calculate_empty():
    assert calculate_total([]) == 0