#!/usr/bin/env python3
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
        try:
            return env(expr)
        except:
            pass

        if isinstance(expr, (tuple, list)):
            op, rest = expr[0], expr[1:]

            if op == if_:
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
# This won't work in python.
Y = (lam, "h",
        ((lam, "x",
            ("h", ("x", "x"))),
            (lam, "x",
                ("h", ("x", "x")))))
