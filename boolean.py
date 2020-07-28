from stlc import if_, lam

not_ = (lam, "a",
        (if_, "a",
            False,
            True))

or_ = (lam, ("a", "b"),
        (if_, "a",
            True,
            (if_, "b",
                True,
                False)))

and_ = (lam, ("a", "b"),
        (if_, "a",
            (if_, "b",
                True,
                False),
            False))
