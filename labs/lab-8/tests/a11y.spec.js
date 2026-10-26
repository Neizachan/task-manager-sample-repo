// Lab 8 steps 6-9: axe-core scan, results exported as JSON to results/axe-<label>.json.
//   $env:A11Y_FIX=""          -> "before" scan      (label "none")
//   $env:A11Y_FIX="lang,alt"  -> "after" scan       (label "lang-alt")
const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('fs');
const path = require('path');

test('axe scan (WCAG 2.0 A + AA)', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
  const label = (process.env.A11Y_FIX || 'none').replace(/[^a-z0-9]+/gi, '-');
  fs.mkdirSync('results', { recursive: true });
  fs.writeFileSync(path.join('results', `axe-${label}.json`), JSON.stringify(results.violations, null, 2));
  console.log(`axe-${label}: ${results.violations.length} violated rules`);
  expect(results.violations, 'accessibility violations found').toEqual([]);
});
