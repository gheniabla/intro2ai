# mathkit — project notes for Claude Code

Tiny pricing toolkit used in CSCI 250 Lab A6.

## How to run tests
```bash
python -m pytest -q
```

## The task
Implement `best_price(price, coupons)` in `mathkit/discounts.py` so the
failing tests in `tests/test_discounts.py` pass. Keep the signature.
Reuse `apply_discount` where it makes sense. Do not edit the tests.

## Conventions
- Prices are rounded to 2 decimals and never negative.
- No new dependencies.
