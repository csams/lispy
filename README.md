This is a bare bones "lisp" written in python. I was inspired by William Byrd's
["The Most Beautiful Program Ever Written" on youtube](https://www.youtube.com/watch?v=OyfBQmvr2Hc).

See also the [Y and Z combinators](https://en.wikipedia.org/wiki/Fixed-point_combinator#Fixed-point_combinators_in_lambda_calculus).

```python
#!/usr/bin/env python3
from lispy import evaluate, if_, lam, Z, add, mul, sub, lt, eq

# Yes, these are tuples.

# The factorial function. Defined in this funny way since simply
# typed lambda calculus doesn't support recursion.
fac_ = (lam, ("f"),
        (lam, ("n"),
            (if_, (eq, "n", 0),
                1,
                (mul,
                    "n",
                    ("f", (sub, "n", 1))))))


# The fibonacci function.
fib_ = (lam, ("f"),
        (lam, ("n"),
            (if_, (lt, "n", 2),
                "n",
                (add,
                    ("f", (sub, "n", 1)),
                    ("f", (sub, "n", 2))))))

# Z will pass fac_ into itself as the first argument.
fac = (Z, fac_)

# Z will pass fib_ into itself as the first argument.
fib = (Z, fib_)

print([(i, evaluate((fac, i))) for i in range(0, 11)])
print([(i, evaluate((fib, i))) for i in range(0, 11)])
```

Output:
```
[(0, 1), (1, 1), (2, 2), (3, 6), (4, 24), (5, 120), (6, 720), (7, 5040), (8, 40320), (9, 362880), (10, 3628800)]
[(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (6, 8), (7, 13), (8, 21), (9, 34), (10, 55)]
```
