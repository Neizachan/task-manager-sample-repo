"""Lab 3 - manually designed EP/BVA tests for app.tasks.calculate_discount.

Specification (derived from the docstring; assumptions A1-A4 in labs/lab-3/lab3_report.md):
  calculate_discount(price, is_premium)
    * price       : real number >= 0   (A1: no upper bound)
    * is_premium  : bool
    * premium     -> price * 0.8       (20 % loyalty discount)
    * non-premium -> price unchanged
    * negative price        -> ValueError   (A2)
    * non-numeric price     -> TypeError    (A3)
    * non-bool is_premium   -> TypeError    (A4)

Cases that currently FAIL against the implementation are marked xfail(strict=True)
so the suite stays green but the defect is documented; strict=True makes the
suite go red the moment the defect is fixed, forcing the marker to be removed.
"""
import pytest
from app.tasks import calculate_discount

D1 = pytest.mark.xfail(strict=True, reason="DEFECT L3-D1: negative price accepted, no ValueError")
D2 = pytest.mark.xfail(strict=True, reason="DEFECT L3-D2: non-numeric price not rejected (non-premium path returns it unchanged)")
D3 = pytest.mark.xfail(strict=True, reason="DEFECT L3-D3: non-bool is_premium silently treated by truthiness")


# ---- valid partitions + boundaries (TC01-TC08, TC16-TC17) -----------------
@pytest.mark.parametrize(
    "tc, price, premium, expected",
    [
        ("TC01", 100, True, 80),          # typical premium
        ("TC02", 100, False, 100),        # typical regular
        ("TC03", 0, True, 0),             # lower boundary, premium
        ("TC04", 0, False, 0),            # lower boundary, regular
        ("TC05", 0.01, True, 0.008),      # just inside lower boundary, premium
        ("TC06", 0.01, False, 0.01),      # just inside lower boundary, regular
        ("TC07", 19.99, True, 15.992),    # fractional price
        ("TC08", 1_000_000_000, True, 800_000_000),  # very large value
    ],
)
def test_valid_prices(tc, price, premium, expected):
    assert calculate_discount(price, premium) == pytest.approx(expected)


def test_regular_user_gets_exact_same_object_value():
    """TC09: non-premium result is identical to input (no float drift)."""
    assert calculate_discount(19.99, False) == 19.99


# ---- invalid price: negative (just outside boundary) ---------------------
@pytest.mark.parametrize(
    "tc, price, premium",
    [
        pytest.param("TC10", -0.01, True, marks=D1),    # just outside boundary
        pytest.param("TC11", -0.01, False, marks=D1),
        pytest.param("TC12", -100, True, marks=D1),     # clearly invalid
    ],
)
def test_negative_price_rejected(tc, price, premium):
    with pytest.raises(ValueError):
        calculate_discount(price, premium)


# ---- invalid price: wrong type -------------------------------------------
@pytest.mark.parametrize(
    "tc, price, premium",
    [
        ("TC13", "abc", True),                         # passes only by accident (str * float -> TypeError)
        pytest.param("TC14", "abc", False, marks=D2),  # returned silently
        pytest.param("TC15", None, False, marks=D2),
    ],
)
def test_non_numeric_price_rejected(tc, price, premium):
    with pytest.raises(TypeError):
        calculate_discount(price, premium)


# ---- invalid is_premium ---------------------------------------------------
@pytest.mark.parametrize(
    "tc, premium",
    [
        pytest.param("TC16", None, marks=D3),
        pytest.param("TC17", "yes", marks=D3),
    ],
)
def test_non_bool_flag_rejected(tc, premium):
    with pytest.raises(TypeError):
        calculate_discount(100, premium)
