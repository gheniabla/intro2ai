"""Pricing helpers.

`apply_discount` already works and has passing tests.
`best_price` is INCOMPLETE — your Lab A9 task is to finish it (with AI help)
so the failing tests in tests/test_discounts.py pass. Keep the signatures.
"""


def apply_discount(price, percent_off):
    """Apply a single percent-off discount.

    price: non-negative number.
    percent_off: int/float percent (e.g. 25 means 25%% off).
    Returns the new price, never negative, rounded to 2 decimals.
    """
    if price < 0:
        raise ValueError("price must be non-negative")
    result = price * (1 - percent_off / 100)
    return round(max(result, 0.0), 2)


def best_price(price, coupons):
    """Apply the SINGLE BEST coupon from a list of percent-off values.

    price:   non-negative number.
    coupons: list of percent-off values (ints/floats). May be empty.

    Rules (see tests/test_discounts.py):
      * empty list  -> price unchanged (rounded to 2 dp)
      * otherwise   -> apply only the largest discount
      * never return a negative number
      * round to 2 decimals

    TODO (Lab A9): implement this. Hint: you can reuse apply_discount().
    """
    raise NotImplementedError("best_price is your Lab A9 task")
