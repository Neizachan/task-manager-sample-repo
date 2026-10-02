# Lab 4 – Requirements Traceability & Test Management
System under specification: **Library System** (requirements supplied in the module slides, "Sample Requirements", 8 items, REQ-001 to REQ-008).
Important: there is **no Library System code** in the repo, so test cases are *designed* (specification-level) and every status is "Designed - not executed". Items marked `[ASSUMPTION]` are where the requirement is silent and need confirming with your instructor.
Machine-readable copies: `rtm.csv`, `test_cases.csv`, `defect_log.csv` (open in Excel). Regenerate with `python labs/lab-4/build_lab4.py`.

## 1. Test case design (31 cases, >= 2 per requirement, every requirement has at least one positive and one negative)
Type: P = positive, N = negative, B = boundary.

| TC ID | Req | Type | Level | Scenario / input | Expected result |
|---|---|---|---|---|---|
| TC-001-01 | REQ-001 | P | System | Register new email nina@example.com, password 'Passw0rd' (exactly 8 chars) | Account created; user can log in. (Boundary: minimum valid length) |
| TC-001-02 | REQ-001 | N | Unit | Register with password 'Pass0rd' (7 chars) | Registration rejected with a message about the 8-character minimum; no account created. (Boundary: just below minimum) |
| TC-001-03 | REQ-001 | N | Unit | Register with an empty password | Registration rejected; no account created |
| TC-002-01 | REQ-002 | P | Integration | Register a second user with a different, unused email | Account created (no false 'already in use' rejection) |
| TC-002-02 | REQ-002 | N | Integration | Register with an email that already has an account | Registration rejected; error message states the email is already in use; still exactly one account for that email |
| TC-002-03 | REQ-002 | N | Integration | Register 'NINA@Example.com' when 'nina@example.com' exists  [ASSUMPTION: emails are case-insensitive] | Rejected as duplicate |
| TC-003-01 | REQ-003 | P | Integration | Search catalogue by exact title of an existing book | That book is in the results |
| TC-003-02 | REQ-003 | P | Integration | Search by author name that has 2 books in catalogue | Both books returned |
| TC-003-03 | REQ-003 | P | Integration | Search by a valid ISBN | Exactly the matching book returned |
| TC-003-04 | REQ-003 | B | Performance | Search with a catalogue of >=10,000 records (measure 20 runs) | Results returned in <= 2 seconds every run (boundary: 2.0 s) |
| TC-003-05 | REQ-003 | N | System | Submit an empty search box  [ASSUMPTION: requirement silent] | No crash and no full-catalogue dump; user is prompted to enter a term |
| TC-004-01 | REQ-004 | P | System | Search for 'zzzzqqqq' (matches nothing) | Message 'No results found' displayed, empty result list |
| TC-004-02 | REQ-004 | N | System | Search for a term that has matches | 'No results found' is NOT displayed |
| TC-004-03 | REQ-004 | N | System | Search for an ISBN that is well-formed but not in the catalogue | 'No results found' displayed |
| TC-005-01 | REQ-005 | P | System | Logged-in user with 0 loans borrows 1 available book | Loan created; due date = borrow date + 14 days; book becomes unavailable |
| TC-005-02 | REQ-005 | B | System | User with 2 loans (none overdue) borrows a 3rd available book | Loan created (boundary: 3rd book allowed) |
| TC-005-03 | REQ-005 | N | System | User tries to borrow a book that is already on loan to someone else | Borrow refused: book unavailable; no loan created |
| TC-005-04 | REQ-005 | N | System | Visitor who is not registered / not logged in tries to borrow | Borrow refused; user asked to register or log in |
| TC-006-01 | REQ-006 | N | System | User with 3 books on loan (none overdue) tries to borrow a 4th | Borrow blocked with limit message; still 3 loans (boundary: 3 -> 4) |
| TC-006-02 | REQ-006 | N | System | User with 1 loan, which is overdue by 1 day, tries to borrow another book | Borrow blocked with overdue message; no new loan |
| TC-006-03 | REQ-006 | P | System | User with 2 loans, none overdue, borrows 1 book | Allowed (control: neither blocking condition holds) |
| TC-007-01 | REQ-007 | P | System | Return a book 1 day before the due date | Return accepted; book available again; fine = P0.00 |
| TC-007-02 | REQ-007 | B | Unit | Return a book exactly ON the due date | Accepted; fine = P0.00 (not yet overdue) |
| TC-007-03 | REQ-007 | B | Unit | Return a book 1 day after the due date | Fine = P2.00 |
| TC-007-04 | REQ-007 | P | Unit | Return a book 5 days after the due date | Fine = P10.00 (5 x P2.00); book available again |
| TC-007-05 | REQ-007 | N | System | Return a book that is not on loan / already returned | Rejected with error; availability and fines unchanged |
| TC-008-01 | REQ-008 | P | Integration | Loan due in exactly 2 days; run the notification job | One reminder email sent to the user's address |
| TC-008-02 | REQ-008 | P | Integration | Loan overdue by 1, 2 and 3 days; run job each day | One overdue email on each of the three days (3 in total) |
| TC-008-03 | REQ-008 | N | Integration | Loan due in 3 days; run the job | No email sent (boundary: one day too early) |
| TC-008-04 | REQ-008 | N | Integration | Overdue book is returned; run job the next day | No further overdue email |
| TC-008-05 | REQ-008 | N | Integration | Two overdue books for one user; run job | One email per overdue book (or clearly itemised), none missed  [ASSUMPTION] |

## 2. Requirements Traceability Matrix
| Requirement ID | Requirement Description | Test Case ID(s) | Test Level | Status |
|---|---|---|---|---|
| REQ-001 | The system shall allow a new user to register with a unique email address and a password of at least 8 characters. | TC-001-01, TC-001-02, TC-001-03 | Unit, System | Designed - not executed |
| REQ-002 | The system shall reject registration when the email address is already in use and display an error message. | TC-002-01, TC-002-02, TC-002-03 | Integration | Designed - not executed |
| REQ-003 | The system shall allow users to search the catalogue by title, author, or ISBN and return matching results within 2 seconds. | TC-003-01, TC-003-02, TC-003-03, TC-003-04, TC-003-05 | Integration, Performance, System | Designed - not executed |
| REQ-004 | The system shall display "No results found" when a search returns no matches. | TC-004-01, TC-004-02, TC-004-03 | System | Designed - not executed |
| REQ-005 | A registered user shall be able to borrow up to 3 available books at a time for a 14-day loan period. | TC-005-01, TC-005-02, TC-005-03, TC-005-04 | System | Designed - not executed |
| REQ-006 | The system shall prevent borrowing when the user already has 3 books on loan or an overdue item. | TC-006-01, TC-006-02, TC-006-03 | System | Designed - not executed |
| REQ-007 | The system shall accept a return, update book availability, and calculate any overdue fine at P2.00 per day. | TC-007-01, TC-007-02, TC-007-03, TC-007-04, TC-007-05 | Unit, System | Designed - not executed |
| REQ-008 | The system shall email the user 2 days before the due date and again on each day the book is overdue. | TC-008-01, TC-008-02, TC-008-03, TC-008-04, TC-008-05 | Integration | Designed - not executed |

Coverage: 8/8 requirements traced; 31 test cases; every requirement has >= 1 positive and >= 1 negative/boundary case. Priority High: REQ-001, 002, 003, 005, 006, 007; Medium: REQ-004, REQ-008.

## 3. Mini test plan (IEEE 829 style) – REQ-006 "Prevent borrowing at 3 loans or with an overdue item"
* **Test plan identifier:** TP-LIB-REQ006-001
* **Introduction / scope:** verify borrowing is blocked when a user has 3 books on loan or any overdue item, and allowed otherwise. In scope: borrow action, loan count, overdue check, user-facing message. Out of scope: search, registration, notifications, fines.
* **Test items:** Library System borrowing module (build under test: first integrated build).
* **Features to be tested:** loan-limit rule (3 -> 4 boundary); overdue-item rule; control case that valid borrowing still works (REQ-005 interaction).
* **Features not tested:** email notifications (REQ-008); performance.
* **Approach:** manual system-level test via the UI, supported by DB set-up scripts to create users with 2/3 loans and overdue loans. Test cases: TC-006-01, TC-006-02, TC-006-03 (plus regression TC-005-02).
* **Entry criteria:** REQ-005/006 baselined and approved; borrowing module deployed to the test environment; test data scripts ready; REQ-001 registration/login working.
* **Exit criteria:** all REQ-006 test cases executed and passed; no open Critical/Major defects against REQ-006; regression TC-005-01..04 pass.
* **Suspension / resumption criteria:** suspend if login or the database is unavailable; resume when restored and smoke test passes.
* **Test deliverables:** this plan, test cases, execution log, defect reports, updated RTM.
* **Environment:** test server with seeded database; browser (latest Chrome); system clock adjustable to simulate overdue loans.
* **Responsibilities:** tester executes and logs; test lead triages; developer fixes.
* **Risks:** clock manipulation needed for overdue data; ambiguity on whether "overdue" means due date passed vs. fine owing (assumed: due date passed).
* **Approvals:** test lead / module coordinator.

## 4. Defect log – two sample defects through the full lifecycle
These are **illustrative sample defects** (the lab asks for "two sample defects"); there is no Library System build to find real ones. They are written as if TC-001-02 and TC-007-02 had failed against a hypothetical first build. Lifecycle: New -> Triaged -> Assigned -> Fixed -> Verified -> Closed. Full per-transition log: `defect_log.csv`.

| Defect | Summary | Requirement | Found by | Severity | Priority |
|---|---|---|---|---|---|
| LIB-DEF-001 | 7-character password accepted at registration | REQ-001 | TC-001-02 | Major | P2 |
| LIB-DEF-002 | Book returned on the due date is fined P2.00 (off-by-one) | REQ-007 | TC-007-02 | Critical | P1 |

| Stage | LIB-DEF-001 | LIB-DEF-002 |
|---|---|---|
| New | Tester logs defect with steps and TC reference | Tester logs defect with steps and TC reference |
| Triaged | Confirmed; Major, P2 (security-relevant rule not enforced) | Confirmed; Critical, P1 (users wrongly charged money) |
| Assigned | Registration developer | Returns developer |
| Fixed | Server-side check length >= 8 | days = max(0, return - due); fine = days x P2.00 |
| Verified | TC-001-02 rejected, TC-001-01 accepted | TC-007-01..04 give P0, P0, P2, P10 |
| Closed | Closed after verification | Closed after verification |

## 5. AI-generated RTM vs. mine
Prompt given to Claude: the eight requirements verbatim, "generate a requirements traceability matrix with test cases, level and status". Output (unedited):

| Req | Test Case(s) | Level | Priority | Status |
|---|---|---|---|---|
| REQ-001 | TC-001 register valid email + 8-char password; TC-002 register with 7-char password | System | High | Not run |
| REQ-002 | TC-003 register with duplicate email | System | High | Not run |
| REQ-003 | TC-004 search by title; TC-005 by author; TC-006 by ISBN (results within 2 s) | System | High | Not run |
| REQ-004 | TC-007 search with no matches | System | Medium | Not run |
| REQ-005 | TC-008 borrow one available book; TC-009 borrow three books | System | High | Not run |
| REQ-006 | TC-010 borrow a 4th book; TC-011 borrow with an overdue item | System | High | Not run |
| REQ-007 | TC-012 return a book; TC-013 return an overdue book, check fine | System | High | Not run |
| REQ-008 | TC-014 email 2 days before due; TC-015 email when overdue | System | Medium | Not run |

| Dimension | Mine | AI draft |
|---|---|---|
| Requirements traced | 8/8 | 8/8 |
| Test cases | 31 | 15 |
| Positive + negative per requirement | yes, all 8 | no – REQ-002, 004, 008 have only one case each, and several are one-sided |
| Boundary cases | 7 vs 8 chars, 3 -> 4 loans, due date / +1 day fine, 2-day vs 3-day email, 2.0 s | 7 vs 8 chars and 3rd/4th book only |
| Performance (2 s) | dedicated test TC-003-04 | folded into a functional search test, no measurement |
| Test levels | Unit / Integration / System / Performance | every case labelled System |
| Negative notification cases (no early email, none after return) | TC-008-03, -04 | missing |
| Expected results | explicit per case | not given |
| Assumptions flagged | yes (case-insensitive email, empty search) | none |

Divergence and verdict the AI matrix is complete at requirement level and a fast skeleton, but thinner on negatives, boundaries, levels and expected results. For an audit I would trust mine, because each requirement has explicit expected outcomes and boundary/negative evidence; I would still use the AI draft to check I had not missed a requirement. Caveat: my cases still need confirming against the instructor's definitions (the `[ASSUMPTION]` rows).

## 6. Reflection
The AI matrix diverged mainly in depth: one or two generic cases per requirement, all at System level, with no expected results or negative notification cases. For an audit I would trust the manual matrix because each row can be executed and judged pass/fail.
