# Lab 5 – Test Automation Framework & Self-Healing Locators

**STATUS: scaffold – written but NOT run against a real browser** (the build environment had no browser, Docker or access to the public site). The mirror server logic was verified, and the 5 tests collect. Steps 4 and 6-9 need you to run them and capture screenshots/results.

**Application under test:** https://the-internet.herokuapp.com/login (a public practice site, per your TA).
You can't change a public site, so the drift step (6-8) uses `webapp/login_mirror.py`, a local copy of the same page that lets you rename an element id.

| Item | File |
|---|---|
| Page Object | `labs/lab-5/pages/login_page.py` |
| 5 data-driven tests | `labs/lab-5/test_ui.py` |
| Test data | `labs/lab-5/data/logins.csv` |
| Local mirror (drift) | `webapp/login_mirror.py` |

## A. Baseline on the public site (steps 1-4)
```powershell
pip install selenium pytest
pytest labs/lab-5/test_ui.py -v
```
Needs Chrome installed (Selenium 4 downloads the driver itself). Expect 5 passed -> screenshot `labs\lab-5\screenshots\baseline-pass.png`.
If the site is slow/unreachable, retry; if a message differs, check the page by hand and fix `logins.csv`.

## B. Healenium (step 5)
Install Docker Desktop, then follow the official self-hosted Healenium setup (clone healenium-web, `docker-compose up`). Note the **proxy URL** it exposes (commonly http://localhost:8085).
**Important:** Healenium can only heal a locator it has seen working. So first run the tests **through the proxy against the unchanged mirror** (that stores the good locators):
```powershell
python -m webapp.login_mirror                       # terminal 1, leave running
$env:HEALENIUM_URL="http://localhost:8085"          # terminal 2
$env:APP_URL="http://host.docker.internal:5000"     # lets the Docker browser reach your PC
pytest labs/lab-5/test_ui.py -v                     # should be 5 passed
```

## C. Drift (steps 6-8)
1. Stop the mirror (Ctrl+C) and restart it with a renamed id:
   ```powershell
   $env:USERNAME_ID="user-name"; python -m webapp.login_mirror
   ```
2. **Without Healenium** (new terminal, so the variable is not set):
   ```powershell
   $env:APP_URL="http://127.0.0.1:5000"
   Remove-Item Env:HEALENIUM_URL -ErrorAction SilentlyContinue
   pytest labs/lab-5/test_ui.py -v
   ```
   Expect all 5 to fail with `NoSuchElementException` for `#username` (it is a plain lookup, no wait) -> screenshot `drift-fail.png` (save the output as the before/after failure report).
3. **With Healenium:** set `HEALENIUM_URL` and `APP_URL=http://host.docker.internal:5000` again, rerun, and screenshot the result as `healed.png` plus the Healenium dashboard/logs as `dashboard.png`.

## D. Write-up (step 9) -> `labs/lab-5/analysis.md`
Record: how many of the 5 tests healed, whether it picked the right element (the renamed username box vs. the password box), and any failures. Then answer the reflection: *what kinds of UI changes would self-healing handle well, and which need a human?* (own words).

Tip: if Healenium setup eats your time, tell your TA – the Page Object, data-driven tests and the drift failure report (A and C2) are still real evidence.

## If the public site is slow or flaky
the-internet.herokuapp.com runs on a free host and can be slow (a first run took ~3.5 min). The page object now waits up to 30 s. If it still fails, check the page loads in your own browser, rerun, or run the baseline against the local mirror instead (`python -m webapp.login_mirror`, then `$env:APP_URL="http://127.0.0.1:5000"`) and say so in your write-up.
