# Lab 6 – AI-Generated Test Cases & Coverage Delta

## 1. Setup
* AI assistant: Claude (chat). Manual tests written separately without AI-style generation (see disclosure in the final message / your README).
* Tools: pytest 9.1, pytest-cov 7.1 (`--cov-branch`), freezegun (to control the clock).
* **Target functions (no tests existed before this lab):** `app.storage.days_until_due`, `app.storage.build_query`, `app.cli.main`.
  (`remove_task`, `find_task_by_title`, `format_task_report` and `save/load_tasks` were already exercised by the task-manager requirement tests (tests/test_task_manager_requirements.py), so they were not eligible.)
* Reproduce:
  `python -m pytest tests/test_lab6_ai.py --cov=app --cov-branch` (AI) · `tests/test_lab6_manual.py` (manual) · both (combined).
  Per-function figures: `python labs/lab-6/func_coverage.py labs/lab-6/cov_<ai|manual|combined>.json`.

## 2. Step 4 – errors fixed so the generated tests execute
None were needed: all 9 AI tests ran and passed first time (`pytest tests/test_lab6_ai.py` -> 9 passed).

## 3. Results
| Run | Tests executed | Line coverage of 3 target functions | Branch cov. (app/cli.py, app/storage.py) | Result |
|---|---|---|---|---|
| AI-only | 9 | 9/9 = **100 %** | 83 % / 100 % | 9 pass |
| Manual-only | 22 cases (20 pass, 2 xfail) | 9/9 = **100 %** | 83 % / 100 % | |
| Combined | 31 cases | 9/9 = **100 %** | 83 % / 100 % | |

(The 17 % gap in `cli.py` is the `if __name__ == "__main__"` guard, identical for every suite. Raw outputs: `coverage_*.txt`, `function_coverage_*.txt`, `cov_*.json`.)

## 4. Comparison – assertion strength
| | AI-generated | Manual |
|---|---|---|
| Distinct test functions / parametrised cases | 9 / 9 | 11 functions / 22 cases |
| `days_until_due` | exact values, but clock frozen at **00:00** only | exact values at **10:30**, leap day, year boundary, 6 bad inputs |
| `build_query` | 1 exact-match test; 2 weak (`startswith("SELECT * FROM tasks")`, `"O'Brien" in query`) | exact strings; apostrophe and injection cases (xfail) |
| `main` | substring checks (`"Loaded 0 tasks" in out`) | exact stdout equality |
| Assertion strength | **mixed: weak on 3 of 9 tests** | strong |

Weak-assertion examples from the AI file:
* `assert query.startswith("SELECT * FROM tasks")` – passes for any query that begins correctly, even one that ignores the title.
* `assert "O'Brien" in build_query("O'Brien")` – this *enshrines the unescaped-quote behaviour as expected* instead of flagging it as a SQL-injection hazard.
* `assert "Pending tasks: 1" in out` – never checks the report lines `main` prints.

## 5. Defects found by this lab's tests
| ID | Defect | Found by | Status |
|---|---|---|---|
| DEF-003 | `days_until_due` subtracts `datetime.now()` (has a time of day) from a midnight date: due **today** returns -1, due tomorrow returns 0, etc. Seven manual cases failed (`manual_run_before_fix.txt`). The AI suite missed it because it froze the clock at exactly 00:00. | manual tests | **Fixed** – compare `date` objects (`date.today()`). |
| DEF-004 | `build_query` concatenates user input into SQL (injection; also breaks on any apostrophe). | manual tests | Open, documented as `xfail`; planned for Lab 12. |

## 6. Verdict (draft)
The AI tests reached the same 100 % line coverage as the manual ones but were weakest where the *input choice* mattered (the midnight clock hid DEF-003) and where they asserted loosely (substring checks, a test that blesses the injection-prone output). Coverage did not distinguish the suites at all – mutation testing (Lab 7) does.

## 7. Reflection (DRAFT – rewrite in your own words)
Yes: the AI suite had full line coverage with several weak assertions, e.g. `"O'Brien" in build_query("O'Brien")`, which only checks the title appears and passes for unsafe SQL.
