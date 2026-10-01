"""Generates rtm.csv, test_cases.csv, defect_log.csv from one data structure so all deliverables stay consistent."""
import csv, pathlib
out = pathlib.Path(__file__).parent

REQS = [
 ("REQ-001","User registration","The system shall allow a new user to register with a unique email address and a password of at least 8 characters.","High"),
 ("REQ-002","User registration","The system shall reject registration when the email address is already in use and display an error message.","High"),
 ("REQ-003","Book search","The system shall allow users to search the catalogue by title, author, or ISBN and return matching results within 2 seconds.","High"),
 ("REQ-004","Book search",'The system shall display "No results found" when a search returns no matches.',"Medium"),
 ("REQ-005","Book borrowing","A registered user shall be able to borrow up to 3 available books at a time for a 14-day loan period.","High"),
 ("REQ-006","Book borrowing","The system shall prevent borrowing when the user already has 3 books on loan or an overdue item.","High"),
 ("REQ-007","Return processing","The system shall accept a return, update book availability, and calculate any overdue fine at P2.00 per day.","High"),
 ("REQ-008","Overdue notifications","The system shall email the user 2 days before the due date and again on each day the book is overdue.","Medium"),
]
# (id, req, type P/N/B, level, scenario & input, expected)
TC = [
 ("TC-001-01","REQ-001","P","System","Register new email nina@example.com, password 'Passw0rd' (exactly 8 chars)","Account created; user can log in. (Boundary: minimum valid length)"),
 ("TC-001-02","REQ-001","N","Unit","Register with password 'Pass0rd' (7 chars)","Registration rejected with a message about the 8-character minimum; no account created. (Boundary: just below minimum)"),
 ("TC-001-03","REQ-001","N","Unit","Register with an empty password","Registration rejected; no account created"),
 ("TC-002-01","REQ-002","P","Integration","Register a second user with a different, unused email","Account created (no false 'already in use' rejection)"),
 ("TC-002-02","REQ-002","N","Integration","Register with an email that already has an account","Registration rejected; error message states the email is already in use; still exactly one account for that email"),
 ("TC-002-03","REQ-002","N","Integration","Register 'NINA@Example.com' when 'nina@example.com' exists  [ASSUMPTION: emails are case-insensitive]","Rejected as duplicate"),
 ("TC-003-01","REQ-003","P","Integration","Search catalogue by exact title of an existing book","That book is in the results"),
 ("TC-003-02","REQ-003","P","Integration","Search by author name that has 2 books in catalogue","Both books returned"),
 ("TC-003-03","REQ-003","P","Integration","Search by a valid ISBN","Exactly the matching book returned"),
 ("TC-003-04","REQ-003","B","Performance","Search with a catalogue of >=10,000 records (measure 20 runs)","Results returned in <= 2 seconds every run (boundary: 2.0 s)"),
 ("TC-003-05","REQ-003","N","System","Submit an empty search box  [ASSUMPTION: requirement silent]","No crash and no full-catalogue dump; user is prompted to enter a term"),
 ("TC-004-01","REQ-004","P","System","Search for 'zzzzqqqq' (matches nothing)","Message 'No results found' displayed, empty result list"),
 ("TC-004-02","REQ-004","N","System","Search for a term that has matches","'No results found' is NOT displayed"),
 ("TC-004-03","REQ-004","N","System","Search for an ISBN that is well-formed but not in the catalogue","'No results found' displayed"),
 ("TC-005-01","REQ-005","P","System","Logged-in user with 0 loans borrows 1 available book","Loan created; due date = borrow date + 14 days; book becomes unavailable"),
 ("TC-005-02","REQ-005","B","System","User with 2 loans (none overdue) borrows a 3rd available book","Loan created (boundary: 3rd book allowed)"),
 ("TC-005-03","REQ-005","N","System","User tries to borrow a book that is already on loan to someone else","Borrow refused: book unavailable; no loan created"),
 ("TC-005-04","REQ-005","N","System","Visitor who is not registered / not logged in tries to borrow","Borrow refused; user asked to register or log in"),
 ("TC-006-01","REQ-006","N","System","User with 3 books on loan (none overdue) tries to borrow a 4th","Borrow blocked with limit message; still 3 loans (boundary: 3 -> 4)"),
 ("TC-006-02","REQ-006","N","System","User with 1 loan, which is overdue by 1 day, tries to borrow another book","Borrow blocked with overdue message; no new loan"),
 ("TC-006-03","REQ-006","P","System","User with 2 loans, none overdue, borrows 1 book","Allowed (control: neither blocking condition holds)"),
 ("TC-007-01","REQ-007","P","System","Return a book 1 day before the due date","Return accepted; book available again; fine = P0.00"),
 ("TC-007-02","REQ-007","B","Unit","Return a book exactly ON the due date","Accepted; fine = P0.00 (not yet overdue)"),
 ("TC-007-03","REQ-007","B","Unit","Return a book 1 day after the due date","Fine = P2.00"),
 ("TC-007-04","REQ-007","P","Unit","Return a book 5 days after the due date","Fine = P10.00 (5 x P2.00); book available again"),
 ("TC-007-05","REQ-007","N","System","Return a book that is not on loan / already returned","Rejected with error; availability and fines unchanged"),
 ("TC-008-01","REQ-008","P","Integration","Loan due in exactly 2 days; run the notification job","One reminder email sent to the user's address"),
 ("TC-008-02","REQ-008","P","Integration","Loan overdue by 1, 2 and 3 days; run job each day","One overdue email on each of the three days (3 in total)"),
 ("TC-008-03","REQ-008","N","Integration","Loan due in 3 days; run the job","No email sent (boundary: one day too early)"),
 ("TC-008-04","REQ-008","N","Integration","Overdue book is returned; run job the next day","No further overdue email"),
 ("TC-008-05","REQ-008","N","Integration","Two overdue books for one user; run job","One email per overdue book (or clearly itemised), none missed  [ASSUMPTION]"),
]
LEVELS = {"REQ-001":"Unit, System","REQ-002":"Integration","REQ-003":"Integration, Performance, System","REQ-004":"System",
          "REQ-005":"System","REQ-006":"System","REQ-007":"Unit, System","REQ-008":"Integration"}
STATUS = "Designed - not executed"

with open(out/"test_cases.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Test Case ID","Requirement ID","Type (P=positive, N=negative, B=boundary)","Level","Scenario / input","Expected result","Status"])
    for t in TC: w.writerow([*t,STATUS])
with open(out/"rtm.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Requirement ID","Requirement Description","Priority","Test Case ID(s)","Test Level","Status"])
    for r in REQS:
        ids=[t[0] for t in TC if t[1]==r[0]]
        w.writerow([r[0],r[2],r[3],", ".join(ids),LEVELS[r[0]],STATUS])

DEF = [
 ("LIB-DEF-001","New","Tester (student)","Registration accepts a 7-character password 'Pass0rd' and creates the account. Found by TC-001-02. REQ-001.","-","-"),
 ("LIB-DEF-001","Triaged","Test lead","Confirmed reproducible. Weak-password rule not enforced on the server.","Major","P2"),
 ("LIB-DEF-001","Assigned","Test lead","Assigned to registration developer.","Major","P2"),
 ("LIB-DEF-001","Fixed","Developer","Server-side length check (>= 8) added; error message shown.","Major","P2"),
 ("LIB-DEF-001","Verified","Tester (student)","Re-ran TC-001-02 (rejected) and TC-001-01 (8 chars accepted).","Major","P2"),
 ("LIB-DEF-001","Closed","Test lead","Verified in build; closed.","Major","P2"),
 ("LIB-DEF-002","New","Tester (student)","Book returned exactly on the due date is charged P2.00 instead of P0.00 (off-by-one in overdue-days calculation). Found by TC-007-02. REQ-007.","-","-"),
 ("LIB-DEF-002","Triaged","Test lead","Confirmed. Users are wrongly charged money.","Critical","P1"),
 ("LIB-DEF-002","Assigned","Test lead","Assigned to returns developer.","Critical","P1"),
 ("LIB-DEF-002","Fixed","Developer","Overdue days = max(0, return_date - due_date); fine = days x 2.00.","Critical","P1"),
 ("LIB-DEF-002","Verified","Tester (student)","Re-ran TC-007-01..04: P0, P0, P2, P10 as expected.","Critical","P1"),
 ("LIB-DEF-002","Closed","Test lead","Verified in build; closed.","Critical","P1"),
]
with open(out/"defect_log.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Defect ID","Lifecycle stage","Actor","Notes","Severity","Priority"])
    for d in DEF: w.writerow(d)

# markdown tables for the report
def md(rows,hdr): return "\n".join(["| "+" | ".join(hdr)+" |","|"+"---|"*len(hdr)]+["| "+" | ".join(str(c).replace("|","/") for c in r)+" |" for r in rows])
(out/"_rtm.md").write_text(md([[r[0],r[2],", ".join(t[0] for t in TC if t[1]==r[0]),LEVELS[r[0]],STATUS] for r in REQS],["Requirement ID","Requirement Description","Test Case ID(s)","Test Level","Status"]),encoding="utf-8")
(out/"_tc.md").write_text(md([[t[0],t[1],t[2],t[3],t[4],t[5]] for t in TC],["TC ID","Req","Type","Level","Scenario / input","Expected result"]),encoding="utf-8")
print(len(TC),"test cases;", len({t[1] for t in TC}),"requirements covered")
for r in REQS:
    types=[t[2] for t in TC if t[1]==r[0]]; print(r[0], "P" in types, "N" in types)
