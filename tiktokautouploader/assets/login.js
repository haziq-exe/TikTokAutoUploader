const { chromium } = require('playwright-extra')

// Load the stealth plugin and use defaults (all tricks to hide playwright usage)
// Note: playwright-extra is compatible with most puppeteer-extra plugins
const stealth = require('puppeteer-extra-plugin-stealth')()

// Add the plugin to playwright (any number of plugins can be added)
chromium.use(stealth)

// Define a delay function
function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

// Define a function to check for redirects
async function checkForRedirect(page) {
    const currentUrl = page.url();
    const pattern = /^https:\/\/www\.tiktok\.com\/foryou/;
    return pattern.test(currentUrl);
}

(async () => {
    let redirected = false;
    const browser = await chromium.launch({ headless: false });
    const page = await browser.newPage();
    await page.goto('https://www.tiktok.com/login');

    // Loop until redirect is detected
    while (!redirected) {
        redirected = await checkForRedirect(page);
        if (!redirected) {
            await delay(1000);
        }
    }

    delay(2000)
    const cookies = await page.context().cookies();
    const fs = require('fs');
    fs.writeFileSync('TK_cookies.json', JSON.stringify(cookies, null, 2));

    // Close the browser
    await browser.close();
})();
