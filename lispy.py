#!/usr/bin/env python3
"""
Getting my head around simply typed lambda calculus and lisp interpreters.

This one evaluates arguments before passing them to functions, known as
"applicative order."

Environments are python closures that are called with variable names. They
return values from the lexical scope in which lambdas are defined.

Variable names are python strings, so there can be collisions with string data.
Stick with numbers.

Python because these things aren't slow enough already.
"""
import operator


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
        # assume it's a variable and try to look it up.
        try:
            return env(expr)
        except:
            pass

        if isinstance(expr, tuple):
            op, rest = expr[0], expr[1:]

            # conditionals
            if op == if_:
                test, consequent, alternative = rest
                return ev(consequent, env) if ev(test, env) else ev(alternative, env)

            # build a procedure from a lambda, capturing the current environment.
            if op == lam:
                vs, body = rest

                def procedure(*args):
                    # When invoked, evaluate the lambda's body in an
                    # environment created by extending the environment of
                    # definition with the parameters bound to the caller's
                    # arguments. Multiple parameters should be in a tuple.
                    e = dict(zip(vs if isinstance(vs, tuple) else (vs,), args))
                    return ev(body, lambda y: e[y] if y in e else env(y))
                return procedure

            # procedure application
            proc = ev(op, env)
            args = [ev(r, env) for r in rest]
            return proc(*args)

        # don't know what to do with it - just say it's "self-evaluating"
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


# See https://en.wikipedia.org/wiki/Fixed-point_combinator
# For recursion in strict languages.
v = (lam, "v", (("x", "x"), "v"))
x = (lam, "x", ("f", v))
Z = (lam, "f", (x, x))

# For recursion in lazy languages.
# Won't work with the current impl. Makes neat python core dumps when you blow
# the stack, though.
x = (lam, "x", ("f", ("x", "x")))
Y = (lam, "f", (x, x))
