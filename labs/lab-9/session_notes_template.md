# Session notes – timestamped (copy to session_notes.md and fill in LIVE during the 45 minutes)
Charter: see charter.md.  
 Timer start: 10:35:10:55
 Tester: Onneile J. Kgwatalala
Page tested: http://127.0.0.1:5001 (Task Manager)
Time-box: 20 minutes
 
Source: AI#1–AI#5 = idea came from the AI, SELF = my own idea.
Result: BUG (with severity small / medium / big) or OK (tested, no bug).
 
| # | Time | What I did | What happened | Source | Result | Screenshot |
|---|------|------------|---------------|--------|--------|------------|
| 1 | 10:37 | Added a task with an empty title | Task accepted; list shows "(priority 1)" with no name (happened twice) | SELF#1 | BUG (small/medium?) | |
| 2 | 10:40| Added a very long number as priority (1000000...) | Accepted; the long number stretches the list line | AI#1 | BUG (small) | |
| 3 | 10:43 | Typed `<script>alert(1)</script>` as the title | Shown as plain text, no popup | AI#1 | OK | |
| 4 | 10:45| Typed letters in the priority box | It was not accepted and creadet an error page | AI#2 |Redirected me to an error page which is OK | |
| 5 | 10:48 | Submitted the form and got /add error | "Internal Server Error" on 127.0.0.1:5001/add. What I typed before it | AI#4 | BUG (big) | Screenshot_2026-10-26_084037.png |
| 6 | 10:50 | Added a task with priority 0, and one with 90000 | Both accepted |  SELF |  BUG (no requirement limits priority) | |
| 7 | 10:52 | Added many tasks, clicked Mark done, compared Pending count | Pending showed 11 and matched the 11 undone tasks in the list | AI#2| OK | Screenshot_2026-10-26_084434.png |
| 8 | 10:54 | Clicked "Mark done" twice on the same task | Recorded the same output twice with a severity of 1 | AI#3 |there was no error made | |
