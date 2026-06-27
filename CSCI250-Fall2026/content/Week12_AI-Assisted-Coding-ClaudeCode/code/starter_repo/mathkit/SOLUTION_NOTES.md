# Reference solution (instructor / self-check)

Do not look until you've tried it yourself. One correct `best_price`:

```python
def best_price(price, coupons):
    if not coupons:
        return round(max(price, 0.0), 2)
    return apply_discount(price, max(coupons))
```

Why it passes:
- empty list -> price unchanged, rounded.
- `max(coupons)` is the single best discount.
- `apply_discount` already clamps at 0 and rounds to 2 dp.
