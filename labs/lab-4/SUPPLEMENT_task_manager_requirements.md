# SUPPLEMENT (not the Lab 4 deliverable) – requirement-based tests for the task manager code

> The official Lab 4 requirements are the Library System list; see lab4_report.md. This file keeps the real defects DEF-001/DEF-002 found and fixed in the repo.

No requirements document was supplied with the repo, so the eight functional requirements below were **derived from the README and function docstrings** (assumption – replace with your instructor's document if one was handed out; the IDs/tests map one-to-one and are easy to re-label).

## 1. Requirements
| ID | Requirement |
|---|---|
| R1 | The system shall create a task with a title, default priority 1, empty tag list, `done = False`, and an id that is **unique** among existing tasks |
| R2 | The system shall mark a task done by id and report whether it was found |
| R3 | The system shall return every task that is not done |
| R4 | The system shall return the average priority of all tasks (0 when there are none) |
| R5 | The system shall remove a task by id |
| R6 | The system shall persist tasks to a JSON file and reload them; a missing file yields an empty list |
| R7 | The system shall produce a plain-text report with one `Task #<id>: <title>` line per task |
| R8 | The system shall find the first task with a given title, or `None` |

## 2. Requirements Traceability Matrix (`tests/test_task_manager_requirements.py`)
| Req ID | Description | Test Case ID(s) | Test Level | Status |
|---|---|---|---|---|
| R1 | Create task, defaults, unique id | TC4-01, TC4-02 | Unit | Pass (TC4-02 failed first – DEF-001, fixed) |
| R2 | Complete task by id | TC4-03, TC4-04 | Unit | Pass |
| R3 | List pending tasks | TC4-05 | Unit | Pass (original off-by-one fixed in Lab 2) |
| R4 | Average priority | TC4-06 | Unit | Pass |
| R5 | Remove task | TC4-07 | Unit | Pass |
| R6 | Save / load JSON | TC4-08, TC4-09 | Integration (file system) | Pass |
| R7 | Text report | TC4-10 | Unit (cross-module: tasks -> storage) | Pass (TC4-10 failed first – DEF-002, fixed) |
| R8 | Find by title | TC4-11 | Unit | Pass |

Coverage check: 8/8 requirements have >= 1 test; 11 test cases total.

## 3. Mini test plan (IEEE 829 style) – R1 "Create task with unique id"
* **Test plan identifier:** TP-R1-001
* **Scope:** `app.tasks.add_task` (id generation, defaults) interacting with `remove_task`. Out of scope: persistence, CLI.
* **Items under test:** `app/tasks.py` at the commit after Lab 3.
* **Features to be tested:** default values; id uniqueness after deletions.
* **Approach:** automated pytest unit tests (TC4-01, TC4-02).
* **Entry criteria:** repo builds; `pytest` runs; Labs 1-2 fixes merged; requirement R1 baselined.
* **Exit criteria:** all R1 tests pass; no open High/Critical defects against R1; no regressions in existing suite.
* **Suspension criteria:** test environment cannot import `app`.
* **Test deliverables:** this plan, test file, run logs (`run_before_fix.txt`, `run_after_fix.txt`).
* **Environment:** Python 3.12, pytest 9.
* **Risks:** ids of previously persisted tasks (JSON files) – id scheme change must stay compatible (max+1 is).

## 4. Defect log – full lifecycle
Lifecycle: New -> Triaged -> Assigned -> Fixed -> Verified -> Closed (all dates 2026-10-01; same-session lab).

### DEF-001 – Duplicate task ids after a removal (R1)
| Stage | Detail |
|---|---|
| New | `add_task` uses `len(tasks)+1`. Add A,B,C, remove #1, add D -> ids `[2, 3, 3]`. Found by TC4-02. |
| Triaged | **Severity: High** (data integrity – `complete_task`/`remove_task` act on the first match, the wrong task may be changed). **Priority: P1** |
| Assigned | Student (self) |
| Fixed | `app/tasks.py`: id = `max(existing ids, default=0) + 1` (`fixes.patch`) |
| Verified | TC4-02 passes; full suite 27 passed (`run_after_fix.txt`) |
| Closed | Closed after verification; no regressions |

### DEF-002 – Task report crashes for every task (R7)
| Stage | Detail |
|---|---|
| New | `format_task_report` concatenates `"Task #" + task["id"]` but ids are ints -> `TypeError: can only concatenate str (not "int") to str`. Found by TC4-10; also crashes `python -m app.cli` as soon as any task exists. |
| Triaged | **Severity: High** (feature unusable). **Priority: P1** |
| Assigned | Student (self) |
| Fixed | `app/storage.py`: f-string `f"Task #{task['id']}: {task['title']}"` (`fixes.patch`) |
| Verified | TC4-10 passes; full suite 27 passed |
| Closed | Closed after verification |

(Open defects from Lab 3, L3-D1..D3, remain documented as `xfail`.)

## 5. AI-generated RTM vs. mine
Prompt to Claude: the eight requirements above, "generate a requirements traceability matrix". Output (unedited):

| Req | Test Case(s) | Level | Status |
|---|---|---|---|
| R1 | TC-001 add task with defaults | Unit | Not run |
| R2 | TC-002 complete existing, TC-003 complete missing | Unit | Not run |
| R3 | TC-004 pending list | Unit | Not run |
| R4 | TC-005 average, TC-006 empty list | Unit | Not run |
| R5 | TC-007 remove | Unit | Not run |
| R6 | TC-008 save/load | Integration | Not run |
| R7 | TC-009 report | Unit | Not run |
| R8 | TC-010 find | Unit | Not run |

| Dimension | Mine | AI |
|---|---|---|
| Completeness (every req traced) | 8/8 | 8/8 |
| Tests that exist and run | 11 real tests, IDs match test names | IDs are plausible but point to **nothing** – no test file; status "Not run" |
| Uniqueness requirement (id after removal) | explicit test TC4-02 | absent – "add task with defaults" only |
| Missing-file load | TC4-09 | absent |
| Cross-module level for R7 | noted | all "Unit" |
| Defect linkage | DEF-001/002 | none |

Verdict (draft): the AI matrix is structurally right and fast, but it traces to tests that do not exist and misses the edge-requirements that actually hide the defects; for an audit I would trust mine because each ID resolves to an executable test with recorded results.

## 6. Reflection (DRAFT – rewrite in your own words)
The AI matrix diverged by tracing requirements to coarse, hypothetical tests rather than ones tied to the code. An auditor needs traceability to executable evidence, so the manual matrix is the one to submit.
