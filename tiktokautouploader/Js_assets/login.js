const { chromium } = require('playwright-extra')
const fs = require('fs');

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
    const args = process.argv.slice(2);
    let proxy = null;

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--proxy' && args[i + 1]) {
            try {
                fs.writeFileSync('proxy_data.txt', args[i+1]);
                proxy = JSON.parse(args[i + 1]);  // Parse the proxy string as JSON
            } catch (error) {
                console.error('Failed to parse proxy argument:', error);
            }
        }
    }

    const browserOptions = {
        headless: false,
    };

    if (proxy && proxy.server) {
        browserOptions.proxy = {
            server: proxy.server,
            username: proxy.username || undefined,
            password: proxy.password || undefined,
        }
    }
    let redirected = false;
    const browser = await chromium.launch(browserOptions);
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
    fs.writeFileSync('TK_cookies.json', JSON.stringify(cookies, null, 2));


    await browser.close();
})();
