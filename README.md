# Algorithmetic

Algorithms for arithmetic.

# Why?

1. For fun
2. I had floating-point precision errors and knew that I could improve the precision doing the division by hand. As it's a step-by-step process, I figured it would be fun to write the algorthm for it.

Frankly, given how difficult this actually was, basic arithmetic is all the more impressive in my eyes.

# How does it work?

Think of addition - you align the values (singles, tens, hundreds etc) and then work from right to left, adding the columns together. If the sum is above ten, you 'carry' a value of 1 across with you. These are logical steps that have been coded similarly for addition, subtraction, multiplication and division operations.

Inputs are always strings that represent numbers and outputs are always string sthat represent numbers.

All coded from scratch - no dependencies.

# Result

```
from operations import add, divide, multiply, subtract

assert add("12345", "678910") == "691255"
assert 12345 + 678910 == 691255

assert subtract("12345", "678910") == '-666565'
assert 12345 - 678910 == -666565

assert multiply("12345", "678910") == "8381143950"
assert 12345 * 678910 == 8381143950

assert divide("12345", "678910", max_decimals=25) == "0.0181835589400656935381714"
assert 12345 / 678910 == 0.018183558940065694  # 18 decimals -> fewer decimals than divide method
```

Run tests with `python test_operations.py`.
