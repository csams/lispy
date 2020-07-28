#!/usr/bin/env python3
import operator
from functools import partial


lam = object()
procedure = object()


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

            if op is lam:
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


Y = ((lam, "f",
        (lam, "x",
            ("f", ("x", "x")))),
        (lam, "y",
            ("f", ("y", "y"))))

fac = (lam, "f",
        (lam, "n",
            ("if", ("==", "n", 0),
                1,
                ("*",
                    "n",
                    ("f", ("-", "n", 1))))))

prog = (lam, "n", ((Y, fac), "n"))
import math
# print(evaluate(((fac, math.factorial), 5)))
print(evaluate((prog, 5)))
