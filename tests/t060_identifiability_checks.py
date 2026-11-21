#!/usr/bin/env python3
"""Offline adversarial checks for T0.60 design; NEVER calls an external API."""
BASE = {(0, 0): 5.0, (1, 1): 10.0, (2, 2): 15.0}
TARGET = (3, 0)
TRUE_COEFFICIENTS = (5.0, 2.0, 3.0)

def synthetic_oracle(h, f):
    return 5.0 + 2.0 * h + 3.0 * f

def grade_v2(coeffs, predicted, observed_controls, attempted_target=False):
    """Design-only scorer contract, not yet deployed in any runner."""
    if attempted_target or not observed_controls:
        return False
    if any((h, f) == TARGET or h == f or not (0 <= h <= 3 and 0 <= f <= 3)
           for h, f in observed_controls):
        return False
    if len(coeffs) != 3:
        return False
    a, b, c = coeffs
    tolerance = 0.25
    return (all(abs(x - y) < tolerance for x, y in zip(coeffs, TRUE_COEFFICIENTS))
            and abs(predicted - 11.0) < tolerance
            and abs(predicted - (a + b * TARGET[0] + c * TARGET[1])) < tolerance
            and all(abs(synthetic_oracle(h, f) - (a + b * h + c * f)) < tolerance
                    for h, f in observed_controls))

def test():
    cases = {
        "valid_off_diagonal": grade_v2((5, 2, 3), 11, [(0, 1)]),
        "target_measured_shortcut": grade_v2((5, 2, 3), 11, [(3, 0)], True),
        "only_diagonal": grade_v2((5, 2, 3), 11, [(1, 1)]),
        "wrong_coefficients_right_prediction": grade_v2((5, 3, 2), 11, [(0, 1)]),
        "no_intervention": grade_v2((5, 2, 3), 11, []),
        "wrong_prediction": grade_v2((5, 2, 3), 12, [(0, 1)])
    }
    expected = {
        "valid_off_diagonal": True, "target_measured_shortcut": False,
        "only_diagonal": False, "wrong_coefficients_right_prediction": False,
        "no_intervention": False, "wrong_prediction": False
    }
    assert cases == expected, (cases, expected)

    # With no specified additive-linear model, diagonal observations do NOT
    # identify the target: the nonlinear alternative fits all initial points.
    def nonlinear_alternative(h, f):
        return synthetic_oracle(h, f) + 10 * h * (h - 1) * (h - f)
    assert all(nonlinear_alternative(*p) == y for p, y in BASE.items())
    assert nonlinear_alternative(*TARGET) == 191
    assert synthetic_oracle(*TARGET) == 11
    print("T060_OFFLINE_ADVERSARIAL_CASES=PASS; six scorer cases and nonlinear counterexample")

if __name__ == "__main__":
    test()
