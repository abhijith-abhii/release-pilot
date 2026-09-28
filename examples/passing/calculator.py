def subtotal(prices):
    if any(p < 0 for p in prices):
        raise ValueError("Prices cannot be negative")
    return sum(prices)
