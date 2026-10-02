# Lab 5 – Analysis (fill in after you run it)

## Results (fill in)
| Run | Command / setting | Result | Screenshot |
|---|---|---|---|
| Baseline, public site | `pytest labs/lab-5/test_ui.py -v` | ___ of 5 passed | baseline-pass.png |
| Through Healenium, unchanged mirror (stores locators) | HEALENIUM_URL + APP_URL set | ___ of 5 passed | |
| Drift, WITHOUT Healenium | USERNAME_ID=user-name | ___ of 5 failed (error: ___) | drift-fail.png |
| Drift, WITH Healenium | HEALENIUM_URL set | ___ of 5 healed; healing success rate ___ % | healed.png, dashboard.png |

Did Healenium ever pick the wrong element (e.g. the password box instead of the username box)? ___

## Reflection – "What kinds of UI changes would you expect self-healing locators to handle well, and what kinds would still require a human fix?"

- Handles well: renamed id/class/name, small attribute changes, an element moved a little in the DOM while its tag, text and neighbours stay similar.
- Needs a human: removed elements, changed workflows (new step, MFA, reordered pages), changed meaning/labels, pages with several similar elements (risk of healing to the WRONG one and a false pass), iframes / dynamic content.
