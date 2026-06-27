"""Tests for mathkit.discounts.

Run from starter_repo/:  python -m pytest -q

The apply_discount tests already PASS. The best_price tests FAIL until you
implement best_price() in mathkit/discounts.py (that is Lab A6).
"""
import pytest
from mathkit.discounts import apply_discount, best_price


# ---- apply_discount: these already pass --------------------------------
def test_apply_discount_basic():
    assert apply_discount(100, 25) == 75.0


def test_apply_discount_clamps_at_zero():
    assert apply_discount(50, 200) == 0.0


def test_apply_discount_rejects_negative_price():
    with pytest.raises(ValueError):
        apply_discount(-1, 10)


# ---- best_price: these FAIL until you implement it ---------------------
def test_best_price_empty_coupons_unchanged():
    assert best_price(100, []) == 100.0


def test_best_price_picks_largest_discount():
    assert best_price(100, [10, 25, 5]) == 75.0


def test_best_price_clamps_at_zero():
    assert best_price(50, [200]) == 0.0


def test_best_price_rounds_to_two_decimals():
    assert best_price(19.99, [10]) == 17.99
