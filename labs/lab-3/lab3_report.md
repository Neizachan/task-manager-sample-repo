# Lab 3 – Dynamic Analysis & Test Design Techniques
Target: `calculate_discount(price, is_premium)` in `app/tasks.py`
Run: `python -m pytest tests/test_calculate_discount_lab3.py -v -rxX`

## 1. Specification and assumptions
The repo has only a docstring ("Apply a loyalty discount for premium users"), so the specification was derived from it plus the code (premium -> price x 0.8). Assumptions that are **mine, not the module's**:

| # | Assumption |
|---|-----------|
| A1 | `price` is a real number >= 0 with no upper bound |
| A2 | negative price is invalid -> `ValueError` |
| A3 | non-numeric price is invalid -> `TypeError` |
| A4 | `is_premium` must be a `bool`; anything else -> `TypeError` |

## 2. Equivalence-partition table
| Input | Class | Type | Representative |
|---|---|---|---|
| price | EP1: price = 0 | valid | 0 |
| price | EP2: price > 0 | valid | 100, 19.99 |
| price | EP3: price < 0 | invalid | -100 |
| price | EP4: not a number | invalid | "abc", None |
| is_premium | EP5: True | valid | True |
| is_premium | EP6: False | valid | False |
| is_premium | EP7: not a bool | invalid | None, "yes" |

## 3. Boundary-value table (price, boundary at 0)
| Boundary | Just outside | On boundary | Just inside |
|---|---|---|---|
| lower (0) | -0.01 | 0 | 0.01 |
| upper | none defined (A1) – a large value 1 000 000 000 is used as a stress point | | |

## 4. Test design (17 cases, all in `tests/test_calculate_discount_lab3.py`)
| ID | price | is_premium | Expected | Partition / boundary | Result |
|---|---|---|---|---|---|
| TC01 | 100 | True | 80 | EP2+EP5 | PASS |
| TC02 | 100 | False | 100 | EP2+EP6 | PASS |
| TC03 | 0 | True | 0 | EP1 on-boundary | PASS |
| TC04 | 0 | False | 0 | EP1 on-boundary | PASS |
| TC05 | 0.01 | True | 0.008 | just inside | PASS |
| TC06 | 0.01 | False | 0.01 | just inside | PASS |
| TC07 | 19.99 | True | 15.992 | fractional | PASS |
| TC08 | 1e9 | True | 8e8 | large | PASS |
| TC09 | 19.99 | False | 19.99 exactly | no float drift | PASS |
| TC10 | -0.01 | True | ValueError | just outside | **FAIL (D1)** |
| TC11 | -0.01 | False | ValueError | just outside | **FAIL (D1)** |
| TC12 | -100 | True | ValueError | EP3 | **FAIL (D1)** |
| TC13 | "abc" | True | TypeError | EP4 | PASS (by accident) |
| TC14 | "abc" | False | TypeError | EP4 | **FAIL (D2)** |
| TC15 | None | False | TypeError | EP4 | **FAIL (D2)** |
| TC16 | 100 | None | TypeError | EP7 | **FAIL (D3)** |
| TC17 | 100 | "yes" | TypeError | EP7 | **FAIL (D3)** |

Run result: **16 passed, 7 xfailed** (the 7 failing parametrised cases are TC10-12, 14-16, 17 marked `xfail(strict=True)` so CI stays green and the defect is documented).

## 5. Defects revealed
| ID | Defect | Evidence | Severity |
|---|---|---|---|
| L3-D1 | Negative prices accepted; a premium user is "charged" -80 for -100 | TC10-TC12 | High |
| L3-D2 | Non-numeric price is rejected only on the premium path (str x float raises) and silently returned on the regular path – inconsistent behaviour; TC13 passes only by accident | TC13-TC15 | Medium |
| L3-D3 | `is_premium` is tested by truthiness after the Lab 2 change (`== True` -> `if is_premium`), so `"no"` or `"false"` grants the discount | TC16-TC17 | Medium |

Note on L3-D3: Lab 2's lint fix made this slightly *worse* – it removed the `== True` comparison that happened to reject truthy non-bools like `"yes"`. A good example of a linter-driven change that alters behaviour.

## 6. AI-generated cases vs. manual cases
Prompt: the specification text above, "generate equivalence classes and boundary/edge-case test data" (Claude). Output in `labs/lab-3/ai_generated_discount_cases.py` (27 parametrised cases). Run: 14 pass / 13 fail.

| Aspect | Manual (17) | AI (27) | Comment |
|---|---|---|---|
| Typical premium/regular | yes | yes | overlap |
| Zero boundary (0, 0.01) | yes | yes | overlap |
| Just-outside boundary -0.01 | yes | yes | overlap |
| Large value 1e9 | yes | yes | overlap |
| Fractional price | yes (19.99) | yes (50.5, 0.1) | overlap |
| Exact no-drift check for regular user | yes (TC09) | no | **AI missed** |
| `None` price, non-bool flag `None` / `"yes"` | yes | yes | overlap |
| Numeric string `"100"`, list `[]` as price | no | yes | **AI extra** (valid EP4 members) |
| NaN / inf price | no | yes | **AI extra**, but spec is silent on them (see below) |
| `True` as price; `1` / `0` as is_premium | no | yes | **spec-dependent** – `bool` is an `int` subclass in Python, so these only fail under my assumption A4 / a stricter "number" reading |
| Float precision `0.1 -> 0.08` via `isclose` | partly (approx) | yes | overlap |

Overlap: the AI reproduced **14 of my 17 cases (82 %)**: TC01-TC08, TC10-TC13, TC16-TC17 (or equivalents). It missed **TC09** (exact equality for the regular path) and **TC14/TC15**: it only tried invalid prices with `is_premium=True`, never on the regular-user path, which is exactly where defect L3-D2 hides.

Questionable / unspecified AI suggestions (checked against the spec, not hallucinated outright but not justified by it):
* NaN / inf -> `ValueError`: spec silent; reasonable but an assumption.
* `True` as price -> `TypeError` and `1`/`0` as flag -> `TypeError`: depends on treating `bool`/`int` strictly; the spec does not say so.
* No incorrect arithmetic or wrong boundary values were produced.

## 7. Reflection (DRAFT notes – rewrite in your own words before submitting, per the manual's integrity rule)
* The AI reproduced about 82 % of my manual cases and added 5-6 edge classes (NaN/inf, numeric string, bool-as-int) I had not considered.
* It missed the exact-equality case and could not tell which failures were "accidental passes".
* It never invented a wrong boundary, but several of its expected results rest on assumptions the spec does not contain, so a human has to decide what the spec should say.

Screenshots: see labs/lab-3/screenshots/.