"""Unit tests for maths/prime_check.py (function is_prime).

Author : Aiza Nawaz
Design : see docs/testing_notes.md
Run    : python -m pytest tests/test_aiza_prime_check.py -v

Techniques used (tagged in the comments):
    ECP = Equivalence Class Partitioning
    BVA = Boundary Value Analysis
    EG  = Error Guessing
"""

import pytest

from maths.prime_check import is_prime


# ---------------------------------------------------------------------------
# is_prime: return values for valid input (10 test cases)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "number, expected",
    [
        (0, False),     # BVA: lowest valid input
        (1, False),     # BVA: one has only one factor
        (2, True),      # BVA: smallest prime
        (3, True),      # BVA: second prime (special-cased in the code)
        (4, False),     # BVA: first composite number / even
        (9, False),     # ECP: multiple of 3
        (25, False),    # BVA: 5*5, divisor found by the loop at i
        (49, False),    # BVA: 7*7, divisor found by the loop at i + 2
        (97, True),     # ECP: prime of the form 6k +/- 1 (loop runs fully)
        (7919, True),   # ECP: large prime (1000th prime)
    ],
    ids=["0", "1", "2", "3", "4", "9", "25", "49", "97", "7919"],
)
def test_is_prime_returns_expected_value(number, expected):
    assert is_prime(number) is expected


# ---------------------------------------------------------------------------
# Module level: input validation and contract (10 test cases)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("number", [-1, -19], ids=["minus_1", "minus_19"])
def test_negative_numbers_raise_value_error(number):  # BVA: just below 0
    with pytest.raises(ValueError):
        is_prime(number)


@pytest.mark.parametrize(
    "value",
    [16.1, 5.0, "7", None],
    ids=["float", "whole_float", "string", "none"],
)
def test_non_integer_types_raise_value_error(value):  # ECP: invalid types / EG
    with pytest.raises(ValueError):
        is_prime(value)


def test_error_message_is_meaningful():  # EG: message should explain the problem
    with pytest.raises(ValueError, match="only accepts positive integers"):
        is_prime(-4)


@pytest.mark.parametrize("flag", [True, False], ids=["True", "False"])
def test_bool_inputs_are_treated_as_integers_one_and_zero(flag):  # EG
    # bool is a subclass of int in Python, so True == 1 and False == 0.
    # Neither is prime and neither raises an error.
    assert is_prime(flag) is False


def test_return_type_is_bool():  # ECP: output type
    assert isinstance(is_prime(7), bool)
    assert isinstance(is_prime(8), bool)
