#!/usr/bin/env python3
"""
Trying to get my head around simply typed lambda calculus and lisp style
interpreters. This one evaluates in applicative order.

Strings are treated as variables, so there can be problems if you use them as
data that conflict with variable names in an enclosing scope. Best just stick to
numbers.

Python because these things aren't slow enough already.

Examples::

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
"""
import operator
from functools import partial


if_ = "if"
lam = "lam"

mul = "*"
add = "+"
sub = "-"
div = "/"

lt = "<"
eq = "=="


def evaluate(expression, environment=None):
    def ev(expr, env):
        # environment lookup
        try:
            return env(expr)
        except:
            pass

        if isinstance(expr, (tuple, list)):
            op, rest = expr[0], expr[1:]

            # conditionals
            if op == if_:
                test, consequent, alternative = rest
                return ev(consequent, env) if ev(test, env) else ev(alternative, env)

            # lambdas
            if op == lam:
                v, body = rest

                def procedure(*args):
                    e = dict(zip(v if isinstance(v, (tuple, list)) else [v], args))
                    return ev(body, lambda y: e[y] if y in e else env(y))
                return procedure

            # application
            proc = ev(op, env)
            args = [ev(r, env) for r in rest]
            try:
                return proc(*args)
            except:
                return partial(proc, *args)

        # self-evaluating
        return expr

    # the machine is born knowing a few things.
    env = {
        add: operator.add,
        sub: operator.sub,
        div: operator.floordiv,
        mul: operator.mul,
        lt: operator.lt,
        eq: operator.eq,
    }

    env.update(environment or {})
    return ev(expression, lambda y: env[y])


# The "Z" combinator for recursion in strict languages.
Z = (lam, "f",
        ((lam, "x",
            ("f", ((lam, "v",
                (("x", "x"), "v"))))),
            (lam, "x",
                ("f", ((lam,
                    "v", (("x", "x"), "v")))))))

# The "Y" combinator for recursion in lazy languages.
# Won't work with the current impl. Makes neat python core dumps, though.
Y = (lam, "h",
        ((lam, "x",
            ("h", ("x", "x"))),
            (lam, "x",
                ("h", ("x", "x")))))
