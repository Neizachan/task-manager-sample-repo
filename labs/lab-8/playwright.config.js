// Lab 8 - Playwright config. It starts the Flask sample site itself (port 5001) from the repo root.
// Environment variables set in your terminal are inherited by the site, so LAYOUT_CHANGE / A11Y_FIX work.
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 60000,
  workers: 1,   // one shared in-memory site, so run tests one at a time
  reporter: [['list'], ['html', { open: 'never' }]],
  use: { baseURL: 'http://127.0.0.1:5001' },
  webServer: {
    command: 'python -m webapp.sample_site',
    cwd: '../..',
    url: 'http://127.0.0.1:5001',
    reuseExistingServer: false,
    timeout: 60000,
  },
  projects: [
    { name: 'desktop-visual', testMatch: 'visual.spec.js', use: { browserName: 'chromium', viewport: { width: 1280, height: 720 } } },
    { name: 'mobile-visual',  testMatch: 'visual.spec.js', use: { browserName: 'chromium', viewport: { width: 375, height: 667 } } },
    { name: 'a11y',           testMatch: 'a11y.spec.js',   use: { browserName: 'chromium', viewport: { width: 1280, height: 720 } } },
  ],
});
