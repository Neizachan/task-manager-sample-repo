# Five AI-suggested ideas (written by Claude for this charter – you may use these OR get your own from the prompt in ai_prompt.md; say which in your report)

1. **Data (D) – boundaries and odd values in each field:** empty title, whitespace only, very long title (500+ chars), HTML/script characters, emoji; priority of 0, negative, huge, decimal, text. *Reveals:* missing validation, crashes, layout breaks, wrong data stored.
2. **Function (F) – counter versus list consistency:** add several tasks, complete some, compare the "Pending" number to what the list shows after every action. *Reveals:* off-by-one and stale-state defects.
3. **Operations (O) – real-user sequences:** complete a task twice, click "Mark done" then use the back button, double-click Add, refresh right after submitting. *Reveals:* duplicate submissions, repeat-action errors, state lost or repeated on refresh.
4. **Interfaces (I) – direct URL tampering:** open `/done/999`, `/done/0`, `/done/abc`, `/add` via GET. *Reveals:* unhandled errors, unfriendly error pages, wrong HTTP behaviour.
5. **Time/Structure (T, S) – volume and ordering:** add 30+ tasks, tasks with identical titles, remove-and-add sequences; look at ids, ordering and scrolling. *Reveals:* duplicate or reused ids, ordering problems, performance or layout issues at volume.
