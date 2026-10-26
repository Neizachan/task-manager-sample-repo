# Session report (fill in after the time-box ends)

# Lab 9 – Session Report

**Tester:** Onneile J. Kgwatalala
**Application tested:** Task Manager (http://127.0.0.1:5001)
**Session length:** 20 minutes (10:35 to 10:55)
**Source of test ideas:** 5 ideas from an AI assistant, plus my own ideas


---

## 1. What I tested

I tried to break a small to-do list page. The page lets a user type a task title and a priority, add the task, mark it done, and see a "Pending" count. I tested:

- Adding a task with an empty title
- Unusual priority values (0, 90000 and a very long number)
- Letters in the priority box
- A title containing `<script>alert(1)</script>`
- Clicking "Mark done" twice on the same task
- Adding many tasks and checking the Pending count
- Typing URLs by hand (`/done/999`, `/done/0`, `/done/abc`, `/add`)

## 2. Bugs found

| Bug ID | Description | Severity | Found by | Time | Steps to reproduce |
|---|---|---|---|---|---|
| BUG-1 | A task with an empty title is accepted. The list shows "(priority 1)" with no task name (this happened twice). | Medium | SELF#1 | 10:37 | Leave Title empty and click "Add task". A nameless task appears in the list. |
| BUG-2 | The priority field has no validation or limit. A very long number (1000000...), 0 and 90000 are all accepted, and the long number stretches the list line. | Small | AI#1 | 10:40 | Type a very long number as priority and click "Add task". The task is added and the list line becomes very wide. |
| BUG-3 | Typing letters in the priority box ends in an "Internal Server Error" page at `/add`. The server crashes instead of showing a message such as "please enter a number". | Major | AI#2 | 10:45 to 10:48 | Type letters in the priority box and click "Add task". The browser goes to `/add` and shows Internal Server Error. [CONFIRM: that the crash at 10:48 was caused by the letters test at 10:45] |

Notes on severity:
- **BUG-1 (medium):** the page still works, but a task with no name is useless to the user and shows that the page does not check its input.
- **BUG-2 (small):** the page keeps working and only the layout is affected. Whether 0 or 90000 are wrong depends on the requirements, which do not give a priority range, so those two are only possible problems.
- **BUG-3 (major):** the server crashes on input a normal user could easily type by mistake.

## 3. Things tested where no bug was found

- **Script in title:** `<script>alert(1)</script>` was shown as plain text and no popup appeared, so the page handles this safely.
- **Pending count:** after adding many tasks and marking some done, the Pending number (11) matched the 11 tasks not yet done.
- **Typing URLs by hand:** the page returned "Not Found" for tasks that do not exist and "Method Not Allowed" when `/add` was opened directly. Both are correct behaviour (the `/add` route only accepts the form button), so these are not bugs. [CONFIRM: add these tests to the notes with their times]
- **Clicking "Mark done" twice:** no error appeared. [CONFIRM: say exactly what happened, for example whether the task stayed done and the Pending count stayed correct]

## 4. Where the bugs came from

| Source | Bugs | Percent |
|---|---|---|
| AI ideas | 2 (BUG-2, BUG-3) | 67% |
| My own ideas | 1 (BUG-1) | 33% |
| **Total** | **3** | **100%** |

The very long priority, 0 and 90000 share one cause (no check on priority), so I counted them once as BUG-2 and credited it to the first test that found it. I also counted the letters-in-priority error page and the `/add` crash as one bug, because the page redirected to `/add` after the letters test [CONFIRM]. If these were two separate crashes, the total would be 4 bugs: 3 from AI ideas (75%) and 1 from my own (25%).

## 5. Did the AI's ideas help?

The AI's ideas found the most serious bug, the crash when letters are typed in the priority box, which was the only major bug. They also found the missing priority check. I found the empty-title problem on my own. The AI's ideas gave me a list of things to try, but I still had to decide what counted as a bug, for example that "Not Found" and "Method Not Allowed" were correct behaviour. [Edit this paragraph so it matches what really happened, in your own words.]

## 6. Limits of this session

- The session lasted 20 minutes, not the 45 minutes the lab asks for, so I covered only a part of the page's behaviour. I did not try a very long title, a title with only spaces, a negative priority or a decimal priority.
- There was no written requirement for the priority range, so I could not say for certain that 0 or 90000 were wrong.
- I tested only through the browser, so I could not see the server's error message and cannot say what line of code failed.