<div align="center">
  <h1>tiktokautouploader</h1>
</div>


### AUTOMATE TIKTOK UPLOADS 🤖. USE TRENDING SOUNDS 🔊, ADD WORKING HASHTAGS 💯, SCHEDULE UPLOADS 🗓️, AUTOSOLVES CAPTCHAS 🧠, AND MORE 🎁

[![PyPI version](https://img.shields.io/pypi/v/tiktokautouploader.svg)](https://pypi.org/project/tiktokautouploader/)  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="READMEimage/READMEGIF.gif" alt="" width="900"/>
</p>

## 🚀 Features

- **🔐 Bypass/Auto Solve Captchas:** No need to worry about any captchas interrupting the process, they'll be solved!
- **🎵 Use TikTok Sounds:** Go viral by seamlessly adding popular TikTok sounds to your videos.
- **🗓 Schedule Uploads:** Upload videos at specific times or upto 10 days in advance with our scheduling feature.
- **🔍 Copyright Check:** Ensure your video is safe from copyright claims before uploading.
- **🏷 Add Working Hashtags:** Increase your reach by adding effective hashtags that actually work.
- **⏰ Cutdown on upload time:** Upload to TikTok with way less hassle and much more speed using our library.
- **📝 Upload to different accounts:** Stay organized and on top of multiple different accounts with our multi-account functionality.
- **🤖 Upload with Telegram**: Code can be integrated with Telegram Bot (More info in /TelegramAutomation)

⭐️ If you like this project please feel free to star it, Thank you.

## 📦 Installation

1. **Python Installation:** Install the package using `pip`:

```bash
pip install tiktokautouploader
```

**NOTE:** IF YOU HAVE INSTALLED BEFORE, PLEASE MAKE SURE YOU UPGRADE TO THE LATEST VERSION.

---

## ⚙️ Pre-requisites

1. **Node.js:** You must have Node.js installed on your system, as some parts of this package rely on JavaScript code. If you don't have Node.js installed, you can download it from [nodejs.org](https://nodejs.org/).

   - **Note:** The necessary JavaScript dependencies (`playwright`,`playwright-extra`, `puppeteer-extra-plugin-stealth`) will be AUTOMATICALLY installed the first time you run the function, so you don't need to install them manually. Make sure that `npm` (Node.js package manager) is available in your system's PATH.


2. **Browser Binaries:** If you don't have them already, you'll need to install the browser binaries for `playwright`. This library uses chromium and firefox.

     to do so, just run the following command AFTER installing the package:
        
    ```bash
    python -m playwright install
    ```


## 📝 Quick-Start

**NOTE:** It is highly recommended you read DOCUMENTATION.md before using the library.
The first time you run the code for an account, you will be prompted to log-in, this will only occur the first time the function is used for the account. Check documentation for more info.

## Upload with hashtags

```python
from tiktokautouploader import upload_tiktok

video_path = 'path/to/your/video.mp4'
description = 'Check out my latest TikTok video!'
accountname = 'mytiktokaccount'
hashtags = ['#fun', '#viral']

upload_tiktok(video=video_path, description=description, accountname=accountname, hashtags=hashtags)

```

### Upload with TikTok Sound

```python
upload_tiktok(video=video_path, description=description, accountname=accountname, sound_name='trending_sound', sound_aud_vol='main')
```

PLEASE READ DOCUMENTATION FOR MORE INFO.

### Schedule an Upload

```python
upload_tiktok(video=video_path, description=description, accountname=accountname, schedule='03:10', day=11)
```

PLEASE READ DOCUMENTATION FOR MORE INFO

### Perform Copyright Check Before Uploading

```python
upload_tiktok(video=video_path, description=description, accountname=accountname, hashtags=hashtags, copyrightcheck=True)
```

## 🎯 Why Choose `tiktokautouploader`?

- **No more captchas:** Fully automated uploads without interruptions, If captchas do show up, no worries, they will be solved. (read documentation for more info)
- **Maximize your reach:** Add popular sounds and effective hashtags that work to boost visibility and go viral!
- **Stay compliant:** Built-in copyright checks to avoid unforeseen takedowns.
- **Convenient scheduling:** Post at the right time, even when you're away!
- **Much faster than manually uploading:** Drastically reduce the time you need to upload videos, just click one button and be done much quicker!
- **Upload to different account:** Stay on top of all your TikTok accounts with our multi-account functionality!

## 🛠 Dependencies

This library requires the following dependencies:

- `playwright`
- `requests`
- `Pillow`
- `inference`

These will be automatically installed when you install the package.

## 👤 Author

Created by **Haziq**. Feel free to reach out at [haziqmk123@gmail.com](mailto:haziqmk123@gmail.com)

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
