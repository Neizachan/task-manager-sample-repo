# Lab 8 – Visual Regression & Accessibility Testing
Application under test: `webapp/sample_site.py` (task-manager web page). Tools: Playwright 1.49+ `toHaveScreenshot`, `@axe-core/playwright` 4.10+ (rules tagged WCAG 2.0 A and AA).

## 1. Visual regression
| Item | Value |
|---|---|
| Pages / viewports | home (empty) and home with one task; desktop 1280x720 and mobile 375x667 |
| Baseline command | `npm run baseline` |
| Deliberate change (`LAYOUT_CHANGE=1`) | side margin 16px -> 48px, heading 28px -> 34px, button blue -> red |
| Result of comparison | ___ of 4 tests failed (FILL IN) |
| Pixel difference – home, desktop | ___ % (ratio from Playwright's message x 100) |
| Pixel difference – home, mobile | ___ % |
Observations (what the diff image highlights, whether any change was surprising): ___

## 2. Accessibility scan – before
Command: `npm run test:a11y` -> `results/axe-none.json`; table made with `python triage.py results/axe-none.json`.
Paste the generated table here (FILL IN from your run). Expected from my pre-check: `button-name` (critical, A), `image-alt` (critical, A), `label` (critical, A), `html-has-lang` (serious, A) and, in a real browser, `color-contrast` (serious, AA).

## 3. Triage by WCAG level and impact
| Rule | WCAG success criterion | Level | Impact | Fix |
|---|---|---|---|---|
| html-has-lang | 3.1.1 Language of Page | A | serious | add `lang="en"` to `<html>` |
| image-alt | 1.1.1 Non-text Content | A | critical | add meaningful `alt` text |
| label | 1.3.1 Info and Relationships / 4.1.2 | A | critical | add `<label for=...>` for each input |
| button-name | 4.1.2 Name, Role, Value | A | critical | `aria-label` on the icon-only button |
| color-contrast | 1.4.3 Contrast (Minimum) | AA | serious | grey #aaaaaa on white is about 2.3:1; #595959 gives about 7:1 (AA needs 4.5:1) |
(Mapping from my knowledge of WCAG; check each against the `helpUrl` in your JSON.)

## 4. Fixes applied and rescan
Fixes (at least two required): ___ (e.g. `lang`, `alt`).
| Scan | Violated rules | File |
|---|---|---|
| Before | ___ | axe-none.json |
| After 2 fixes (`A11Y_FIX=lang,alt`) | ___ | axe-lang-alt.json |
| After all fixes (`A11Y_FIX=all`) | ___ | axe-all.json |

## 5. Pre-check done while building this lab (not a substitute for your run)
I ran the real axe-core engine under jsdom (no layout engine, so `color-contrast` is disabled) against each page variant:
```
fix=none     button-name(critical), html-has-lang(serious), image-alt(critical), label(critical)
fix=lang     button-name, image-alt, label
fix=alt      button-name, html-has-lang, label
fix=label    button-name, html-has-lang, image-alt
fix=button   html-has-lang, image-alt, label
fix=all      (none)
```
So each seeded issue is detectable and each switch removes exactly its own rule. The page was written with these defects on purpose; they are not findings about any real product.

## 6. Reflection (DRAFT NOTES – rewrite in your own words)
Question: *Which accessibility violations would a simple pixel-diff visual test never catch, and why does that justify running both?*
- A pixel diff only says "the picture changed". It cannot see missing `alt` text, missing `lang`, unlabeled inputs or an unnamed icon button – these look identical on screen but break screen readers. Removing `lang` or an `aria-label` changes zero pixels.
- Conversely axe cannot see that a button turned red or a margin moved; only the visual test catches layout/styling regressions.
- Low contrast is the overlap: axe measures it numerically, a pixel diff only notices if it *changes*.
