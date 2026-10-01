# Lab 7 – Mutation Testing & Suite Effectiveness

## 1. Setup
* Tool: **mutmut 3.8.0** (primary) and **cosmic-ray** (cross-check). Targets: the 3 Lab 6 functions (39 mutmut mutants: `days_until_due` 9, `build_query` 7, `main` 23).
* Config: `pyproject.toml` (`[tool.mutmut]`; `also_copy = ["pytest.ini"]` is required, otherwise mutmut silently tests the unmutated code). The suite under test is chosen with `pytest_add_cli_args_test_selection`.
* Command (one run per suite):
  `mutmut run "app.storage.x_days_until_due*" "app.storage.x_build_query*" "app.cli.x_main*"` then `mutmut results --all true`.
* **Windows note:** mutmut 3 does not run natively on Windows; use WSL. All results here were produced on Linux, raw output in `labs/lab-7/mutmut_*_results.txt`.

## 2. Mutation scores
| Suite | Killed / Total | Mutation score | Line coverage (Lab 6) |
|---|---|---|---|
| AI-only | 38 / 39 | **97.4 %** | 100 % |
| Manual-only | 39 / 39 | **100 %** | 100 % |
| Combined | 39 / 39 | **100 %** | 100 % |
| AI + targeted tests (final, Step 8) | 39 / 39 | **100 %** | 100 % |

Cross-check with cosmic-ray (33 mutants in the same functions, all three suites): 100 % each, 0 survivors (`cosmic_ray_*_summary.txt`).

**Honest note on Step 6 ("at least three surviving mutants").** These three functions are small and the AI suite is fairly strong, so the tools produced only **one** surviving mutant against the AI suite. I did not invent more. Instead I analysed that one plus a second survivor found by hand: re-introducing the original DEF-003 implementation. If your rubric strictly needs three, run Lab 6/7 on larger functions (see the last section).

## 3. Surviving mutants – why they survived
**M1 – `app.cli.x_main__mutmut_13` (mutmut)**
```diff
-    print(format_task_report(tasks))
+    print(None)
```
The AI tests asserted `"Loaded 2 tasks" in out` and `"Pending tasks: 1" in out` only. Substring checks on two other lines never look at the report body, so replacing the report with `None` still passes. (Line coverage was 100 % – the line ran, nothing verified its output.) Killed by the manual suite, which compares the whole stdout.

**M2 – re-introduced DEF-003 (hand-made mutant, `m2_manual_mutant_check.txt`)**
```diff
-    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
-    return (due_date - datetime.date.today()).days
+    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
+    delta = due_date - datetime.datetime.now()
+    return delta.days
```
Result: AI-only **9 passed** (survives); manual-only 7 failed (killed). The AI tests freeze the clock at exactly 00:00:00, the one instant where the buggy and the fixed code agree, so no assertion could tell them apart.

## 4. New tests that kill them – `tests/test_lab7_targeted.py`
* `test_m1_main_prints_the_report_body` – compares the exact list of printed lines -> kills M1.
* `test_m2_due_today_and_tomorrow_midday` and `test_m2_due_today_just_before_midnight` – clock at 10:30 and 23:59:59 -> kill M2.

Verification: M2 vs AI+targeted: 2 failed (killed). Final mutmut run on AI + targeted: **39/39 killed = 100 %** (`mutmut_ai_plus_targeted_results.txt`).

## 5. Coverage vs. mutation score
Line coverage was 100 % for every suite, yet the AI suite scored 97.4 % and still missed a real defect class (time-of-day, DEF-003). Coverage only says a line *ran*; mutation score says whether a wrong change to it would be *noticed*. A larger spread would be expected on larger functions – here the functions are tiny, so the gap is small but still real.

## 6. Reflection (DRAFT – rewrite in your own words)
The gap between 100 % coverage and 97.4 % mutation score (plus the hand-made DEF-003 mutant) shows coverage overstates test quality: the AI tests executed everything but verified less. Mutation testing exposed *which* assertion was missing.

## 7. If you need three real survivors
Re-run Labs 6-7 against functions with more logic, e.g. `calculate_discount`, `remove_task`, `find_task_by_title` (change `TARGET` globs and the Lab 6 tests accordingly). Those carry more branches and arithmetic mutants for assertion-light tests to miss.
