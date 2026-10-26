// Lab 8 steps 2-5: visual regression with Playwright's built-in screenshot comparison.
//   npm run baseline      -> captures the baseline screenshots (step 3)
//   (set LAYOUT_CHANGE=1) -> npm run test:visual  fails and prints "N pixels (ratio X of all image pixels) are different" (step 5)
const { test, expect } = require('@playwright/test');

test.beforeEach(async ({ request }) => { await request.get('/reset'); });  // clean slate for every test

test('home page matches the baseline', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('home.png', { maxDiffPixelRatio: 0 });   // viewport-sized, so the size never changes
});

test('page with a task matches the baseline', async ({ page }) => {
  await page.goto('/');
  await page.fill('#title', 'Write report');
  await page.click('button[type=submit]');
  await expect(page.locator('.task-title')).toHaveText('Write report');
  await expect(page).toHaveScreenshot('with-task.png', { maxDiffPixelRatio: 0 });
});
