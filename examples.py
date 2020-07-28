#!/usr/bin/env python3
from stlc import evaluate, if_, lam, Z, add, mul, sub, lt, eq

# The factorial function.
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
                1,
                (add,
                    ("f", (sub, "n", 1)),
                    ("f", (sub, "n", 2))))))

# Z will pass fac_ into itself as the first param.
fac = (Z, fac_)

# Z will pass fib_ into itself as the first param.
fib = (Z, fib_)

print([(i, evaluate((fac, i))) for i in range(0, 10)])
print([(i, evaluate((fib, i))) for i in range(0, 10)])