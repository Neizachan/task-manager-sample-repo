# Lab 9 – Exploratory Testing with an AI Co-Pilot (45-minute session + 45-minute report)

**This lab has to be done by you.** The deliverables are your own timestamped notes, the bugs *you* found, and a breakdown of how many came from AI-suggested ideas versus your own instincts. I can't honestly invent that, and your TA would see through it. What I've prepared is everything around the session so you only have to test.

## Do it in this order
1. **Start the app** (repo root): `pip install flask` then `python -m webapp.sample_site` -> open http://127.0.0.1:5001
   (Reload the page's state any time with http://127.0.0.1:5001/reset)
2. **Adopt the charter** in `charter.md` (edit if you want a different feature). 2 minutes.
3. **Get AI ideas BEFORE starting the timer** (manual step 2): paste the prompt in `ai_prompt.md` into your Lab 1 assistant (Claude / ChatGPT / Continue+Ollama), or use the five ideas I pre-filled in `ai_ideas_draft.md` and say so. Save the answer in `ai_ideas.md`. Number the ideas 1-5.
4. **Run a 45-minute timer.** Explore the app. Log EVERYTHING as you go in `session_notes.md` (copy `session_notes_template.md`): time, what you did, what you saw. Tag each line `AI#n` when it came from an AI idea or `SELF` when it's your own idea.
5. **Stop the moment the timer ends.** Then (the 45-minute reporting half) fill in `session_report_template.md` -> `session_report.md`: bugs with severity and source, plus the percentage from AI vs self.
6. **Reflection** (own words): did the AI ideas lead you to bugs you wouldn't have found unprompted?

## Deliverables
- [ ] `charter.md`  - [ ] `session_notes.md` (timestamped)  - [ ] `session_report.md` (bug list, severity, AI-vs-self breakdown)
- [ ] a screenshot or two of bugs in the app (`screenshots/`)

Tips: the page has an add form (title, priority), a pending counter, and a "mark done" link per task. Try odd inputs, repeated actions, the browser's back button, many tasks, long text, and compare what the counter says with what the list shows. Don't read `webapp/sample_site.py` or the app code first – that would spoil the exploration.
