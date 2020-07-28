#!/usr/bin/env python3
import operator
from functools import partial


lam = "lam"


def evaluate(expression, environment=None):
    def ev(expr, env):
        try:
            return env(expr)
        except:
            pass

        if isinstance(expr, (tuple, list)):
            op, rest = expr[0], expr[1:]

            if op == "if":
                test, consequent, alternative = rest
                return ev(consequent, env) if ev(test, env) else ev(alternative, env)

            if op == lam:
                v, body = rest

                def procedure(*args):
                    e = dict(zip(v if isinstance(v, (tuple, list)) else [v], args))
                    return ev(body, lambda y: e[y] if y in e else env(y))
                return procedure

            proc = ev(op, env)
            args = [ev(r, env) for r in rest]
            try:
                return proc(*args)
            except:
                return partial(proc, *args)

        return expr

    env = {
        "+": operator.add,
        "-": operator.sub,
        "/": operator.floordiv,
        "*": operator.mul,
        "<": operator.lt,
        "==": operator.eq,
    }

    env.update(environment or {})
    return ev(expression, lambda y: env[y])


# The "Y" combinator for recursion in lazy languages.
# This won't work in python.
Y = (lam, "h",
        ((lam, "x",
            ("h", ("x", "x"))),
            (lam, "x",
                ("h", ("x", "x")))))

# The "Z" combinator for recursion in strict languages.
# This works in python.
Z = (lam, "f",
        ((lam, "x",
            ("f", ((lam, "v",
                (("x", "x"), "v"))))),
            (lam, "x",
                ("f", ((lam,
                    "v", (("x", "x"), "v")))))))

# The base factorial function
fac = (lam, "f",
        (lam, "n",
            ("if", ("==", "n", 0),
                1,
                ("*",
                    "n",
                    ("f", ("-", "n", 1))))))

# factorial defined with the Z combinator.
fact = (Z, fac)
print(evaluate((fact, 5)))
