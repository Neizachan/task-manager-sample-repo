# Lab 8 – Visual Regression & Accessibility Testing

**STATUS: built and pre-checked, NOT yet run in a real browser.** My workspace has no browser, so the Playwright screenshot comparison and the colour-contrast check are for you to run. What I did verify: the page variants render, and the real axe-core engine (run under jsdom) finds exactly the seeded issues and each fix removes exactly one (see `lab8_report.md`, section 5).

**Tools:** Playwright (`toHaveScreenshot`) for visual regression, `@axe-core/playwright` for accessibility – the two tools named in the manual.
**Application:** `webapp/sample_site.py`, a web front-end for the task manager (port 5001). It ships with deliberate accessibility problems so the scan has something to find. Switches: `LAYOUT_CHANGE=1` (visual change) and `A11Y_FIX=lang,alt,label,button,contrast|all` (fixes).

## Run it (PowerShell, from the repo root)
Needs Node.js (check `node --version`) and `pip install flask`.
```powershell
cd labs\lab-8
npm install
npx playwright install chromium
```
Port 5001 must be free; Playwright starts and stops the site itself.

### Steps 1-3: baseline screenshots
```powershell
npm run baseline
```
Creates baseline images in `tests\visual.spec.js-snapshots\` (desktop 1280x720 and mobile 375x667, two pages each = 4 images). **Commit them.** Screenshot the terminal -> `screenshots\baseline.png`.

### Steps 4-5: deliberate change and diff report
```powershell
$env:LAYOUT_CHANGE="1"
npm run test:visual
Remove-Item Env:LAYOUT_CHANGE
npx playwright show-report
```
`LAYOUT_CHANGE=1` widens the side margin, enlarges the heading and turns the button red. The tests should FAIL with a line like `N pixels (ratio 0.0X of all image pixels) are different` – **write that ratio down; it is your "percentage pixel difference"** (ratio x 100). The HTML report (opens in the browser) shows expected / actual / diff images. Screenshot it -> `screenshots\visual-diff.png`.

### Steps 6-8: accessibility scan
```powershell
npm run test:a11y                 # "before": fails, writes results\axe-none.json
python triage.py results\axe-none.json
```
Paste the table into your report and add your own columns if you like. Screenshot -> `screenshots\axe-before.png`.
Expected rules (pre-checked): `button-name`, `html-has-lang`, `image-alt`, `label`, plus `color-contrast` (needs a real browser, so only you will see it).

### Step 9: fix at least two, rescan
```powershell
$env:A11Y_FIX="lang,alt"
npm run test:a11y                 # fewer violations, writes results\axe-lang-alt.json
$env:A11Y_FIX="all"
npm run test:a11y                 # should pass, writes results\axe-all.json
Remove-Item Env:A11Y_FIX
python triage.py results\axe-lang-alt.json
```
Screenshot each -> `screenshots\axe-after-2.png`, `axe-after-all.png`.
The fixes are one-line changes in `webapp/sample_site.py` (`lang="en"`, `alt=` text, `<label>`s, `aria-label` on the icon button, darker grey text). To make them permanent, copy them into the page and drop the switch.

## Deliverables checklist (from the manual)
- [ ] Visual regression diff report showing the deliberate change (`playwright-report`, screenshot, pixel-difference %)
- [ ] Accessibility scan reports before and after + triage table (`results\*.json`, `lab8_report.md`)
- [ ] Short summary of the two fixes and confirmed resolution
- [ ] Reflection (own words) – draft notes at the end of `lab8_report.md`

## If something goes wrong
- `Port 5001 is already used` -> close the other terminal running the site.
- `Executable doesn't exist` -> run `npx playwright install chromium`.
- Screenshot test fails on the *first* run -> you skipped `npm run baseline`.
- Baselines are OS/browser specific: create and compare them on the same machine.
