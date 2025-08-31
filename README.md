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

# Bonus

## Estimating Pi using perfect precision numbers

A numerical approach to estimating the value of pi is to generate a large number of random co-ordinates between (0, 0) and (1, 1) and calculate if the distance from (0, 0) is greater than 1 (the unit circle radius). Based on the ratio of points that lie inside vs outside the unit-circle, we can estimate `pi`.

This approach usually breaks down because of the limits of floating point arithmetic. However, using this repo's 'perfect precision' techniques, this should not be an issue any longer.

Below is the output of a run with 10M iterations, which estimates `pi` to within 0.0065% of the value hard-coded in the python `math.pi` value.

```
Batch result: inside = 785826, outside = 214174
Batch result: inside = 784965, outside = 215035
Batch result: inside = 785091, outside = 214909
Batch result: inside = 785677, outside = 214323
Batch result: inside = 785616, outside = 214384
Batch result: inside = 785891, outside = 214109
Batch result: inside = 784946, outside = 215054
Batch result: inside = 785354, outside = 214646
Batch result: inside = 785181, outside = 214819
Batch result: inside = 784924, outside = 215076

Estimated value of pi: 3.1413884
Pythonic  value of pi: 3.141592653589793
Accuracy: -0.00650159 %
Final counts: inside = 7853471, outside = 2146529
```
