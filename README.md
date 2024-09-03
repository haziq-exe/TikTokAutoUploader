<div align="center">
  <h1>tiktokautouploader</h1>
</div>


### AUTOMATE TIKTOK UPLOADS. USE TRENDING SOUNDS 🔊, AUTOSOLVES CAPTCHAS 🧠, ADD WORKING HASHTAGS 💯 AND MORE

[![PyPI version](https://img.shields.io/pypi/v/tiktokautouploader.svg)](https://pypi.org/project/tiktokautouploader/) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<p align="center">
  <img src="READMEimage/Image.png" alt="" width="400"/>
</p>

## 🚀 Features

- **🔐 Bypass/Auto Solve Captchas:** No more manual captcha solving; fully automated process!
- **🎵 Use TikTok Sounds:** Seamlessly add popular TikTok sounds to your videos.
- **🗓 Schedule Uploads:** Upload videos at specific times with our scheduling feature.
- **🔍 Copyright Check:** Ensure your video is safe from copyright claims before uploading.
- **🏷 Add Working Hashtags:** Increase your reach by adding effective hashtags that actually work.


## 📦 Installation

Install the package using `pip`:

```bash
pip install tiktokautouploader
```



## ⚙️ Pre-requisites

Before you can use this library you'll NEED to do the following two steps:

⚠️ You'll need to install the necessary browser binaries for `playwright`.

Run the following command AFTER installing the package:

```bash
playwright install
```

⚠️ You'll need to download your tiktok cookies into a .json file after logging into your account on chrome.
NOTE: it is recommended that you use a tiktok account that has at least a week or two of cookies.

❗ How to install your .json cookies file:

• Download the following chrome extension: https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en&pli=1

• Open tiktok.com and log-in

• Once logged in, click on your cookie-editor and click 'Export'. Then export as 'JSON'

• Create a .json file and paste the JSON cookies that you copied with the extension

• Finally, include the path to your cookies file in your function!


## 📝 Quick-Start

Here's how to upload a video to TikTok using `tiktokautouploader`:

```python
from tiktokautouploader import upload_tiktok

video_path = 'path/to/your/video.mp4'
description = 'Check out my latest TikTok video!'
hashtags = ['#fun', '#viral']
cookies_path = 'path/to/your/cookies.json'

upload_tiktok(video=video_path, description=description, hashtags=hashtags, cookies_path=cookies_path)

```

### Upload with TikTok Sound

```python
upload_tiktok(video=video_path, description=description, hashtags=hashtags, cookies_path=cookies_path, sound_name='trending_sound')
```

PLEASE READ DOCUMENTATION FOR MORE INFO.

### Schedule an Upload

```python
upload_tiktok(video=video_path, description=description, hashtags=hashtags, cookies_path=cookies_path, schedule='03:10', day=11)
```

PLEASE READ DOCUMENTATION FOR MORE INFO

### Perform Copyright Check Before Uploading

```python
upload_tiktok(video=video_path, description=description, hashtags=hashtags, cookies_path=cookies_path, copyrightcheck=True)
```

## 🎯 Why Choose `autotiktokuploader`?

- **No more captchas:** Fully automated uploads without interruptions, If captchas do show up, no worries, they will be solved. (read documentation for more info)
- **Maximize your reach:** Add popular sounds and effective hashtags that work to boost visibility.
- **Stay compliant:** Built-in copyright checks to avoid unforeseen takedowns.
- **Convenient scheduling:** Post at the right time, even when you're away.

## 🛠 Dependencies

This library requires the following dependencies:

- `playwright`
- `requests`
- `Pillow`
- `transformers`
- `torch`
- `scikit-learn`
- `inference`

These will be automatically installed when you install the package.

## 👤 Author

Created by **Haziq Khalid**. Feel free to reach out at [haziqmk123@gmail.com](mailto:haziqmk123@gmail.com) or my LinkedIn.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
```
