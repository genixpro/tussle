const { defineConfig } = require("cypress");

module.exports = defineConfig({
  defaultCommandTimeout: 30000,
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
      require('cypress-terminal-report/src/installLogsPrinter')(on);

      on('before:browser:launch', (browser = {}, launchOptions) => {
        /* ... */
        if (browser.family === 'chromium' && browser.name !== 'electron') {
          launchOptions.args.push('--no-sandbox --disable-gpu --disable-dev-shm-usage --disable-software-rasterizer --disable-setuid-sandbox --disable-web-security --disable-features=IsolateOrigins,site-per-process');
        }

        return launchOptions;
      })
    },
  },
});
