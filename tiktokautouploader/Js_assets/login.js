const { chromium } = require('playwright-extra')


const stealth = require('puppeteer-extra-plugin-stealth')()

chromium.use(stealth)


function sleep(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}


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

    while (!redirected) {
        redirected = await checkForRedirect(page);
        if (!redirected) {
            await sleep(1000);
        }
    }

    sleep(2000)
    const cookies = await page.context().cookies();
    const fs = require('fs');
    fs.writeFileSync('TK_cookies.json', JSON.stringify(cookies, null, 2));

    
    await browser.close();
})();
