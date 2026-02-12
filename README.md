<div align="center">
  <h1>tiktokautouploader</h1>
</div>

### AUTOMATE TIKTOK UPLOADS. USE TRENDING/FAVORITED SOUNDS, ADD WORKING HASHTAGS, SCHEDULE UPLOADS, AUTOSOLVES CAPTCHAS, AND MORE

[![PyPI version](https://img.shields.io/pypi/v/tiktokautouploader.svg)](https://pypi.org/project/tiktokautouploader/)

<div align="center">
WORKING AS OF FEB 2026 (sound_aud_vol issues only, use default ```sound_aud_vol='mix'```)
</div>

<p align="center">
  <img src="READMEimage/READMEGIF.gif" alt="" width="900"/>
</p>

## Features

- **Bypass/Auto Solve Captchas:** Captchas won't slow you down, they get solved automatically.
- **Upload with TikTok Sounds:** Add popular TikTok sounds to your videos. Search by name or pull straight from your favorites.
- **Schedule Uploads:** Queue videos for a specific time, up to 10 days out.
- **Copyright Check:** Run a copyright check before uploading so you're not caught off guard later.
- **Add Working Hashtags:** Hashtags that are clickable and actually show up as hashtags instead of text.
- **Proxy Support:** Route your uploads through a proxy server of your choice.
- **Multiple Accounts:** Handle as many TikTok accounts as you need without losing track of any of them.
- **Telegram Integration:** Hook the uploader up to a Telegram bot. Check `/TelegramAutomation` for setup details.

---

## Installation

```bash
pip install tiktokautouploader
```

> **Already installed?** Make sure you're on the latest version before running anything.

---

## Pre-requisites

**Node.js** is required since parts of this package run JavaScript under the hood. Grab it from [nodejs.org](https://nodejs.org/) if you don't have it. The JS dependencies (`playwright`, `playwright-extra`, `puppeteer-extra-plugin-stealth`) install themselves the first time you run the function — just make sure `npm` is in your PATH.

**Browser binaries** also need to be installed once (run after installing library):

```bash
python -m playwright install
```

---

## Quick-Start

> It's worth reading `DOCUMENTATION.md` before diving in. The first time you use the function for an account you'll be asked to log in — this only happens once per account.

NOTE: The first time you run the function, it may take a long while to run as JS libraries are built, this only occurs on first run

### Upload with hashtags

```python
from tiktokautouploader import upload_tiktok

upload_tiktok(
    video='path/to/your/video.mp4',
    description='Check out my latest TikTok video!',
    accountname='mytiktokaccount',
    hashtags=['#fun', '#viral']
)
```

### Upload with a TikTok Sound

```python
# Search for a sound by name (default behaviour)
upload_tiktok(video=video_path, description=description, accountname=accountname,
              sound_name='trending_sound', sound_aud_vol='mix')

# Pull a sound from your TikTok favorites instead
upload_tiktok(video=video_path, description=description, accountname=accountname,
              sound_name='saved_sound', sound_aud_vol='mix', search_mode='favorites')
```

`sound_aud_vol` controls the balance between your video's original audio and the TikTok sound: `'main'`, `'mix'`, or `'background'`. Check the docs for details.

### Schedule an Upload

```python
upload_tiktok(video=video_path, description=description, accountname=accountname,
              schedule='03:10', day=11)
```

### Copyright Check Before Uploading

```python
upload_tiktok(video=video_path, description=description, accountname=accountname,
              hashtags=hashtags, copyrightcheck=True)
```

> The upload will stop if your video fails the copyright check.

### Run Headless with Stealth + Proxy

```python
upload_tiktok(
    video=video_path,
    description=description,
    accountname=accountname,
    headless=True,       # no browser window
    stealth=True,        # human-like delays between actions
    suppressprint=True,  # no console output
    proxy={              # optional proxy config — see docs for format
        'server': 'http://yourproxy:port',
        'username': 'user',
        'password': 'pass'
    }
)
```

---

## Full Parameter Reference

| Parameter | Type | Description |
|---|---|---|
| `video` | `str` | Path to the video file |
| `description` | `str` | Caption for the video |
| `accountname` | `str` | Which account to upload on |
| `hashtags` | `list` *(opt)* | List of hashtags to include |
| `sound_name` | `str` *(opt)* | Name of the TikTok sound to use |
| `sound_aud_vol` | `str` *(opt)* | Audio balance: `'main'`, `'mix'`, or `'background'` |
| `schedule` | `str` *(opt)* | Upload time in `HH:MM` (your local time) |
| `day` | `int` *(opt)* | Day to schedule the upload for |
| `copyrightcheck` | `bool` *(opt)* | Run a copyright check before uploading |
| `suppressprint` | `bool` *(opt)* | Silence all progress output from the function |
| `headless` | `bool` *(opt)* | Run without a visible browser window |
| `stealth` | `bool` *(opt)* | Add delays between operations to mimic human behaviour |
| `proxy` | `dict` *(opt)* | Proxy server config — see docs for the expected format |
| `search_mode` | `str` *(opt)* | How to find the sound: `'search'` (default) or `'favorites'` |

---

## Dependencies

`playwright`, `requests`, `Pillow`, `inference` — all installed automatically with the package.

---