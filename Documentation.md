# autotiktokuploader Documentation

This document provides detailed information about the parameters and usage of the `upload_tiktok` function in the **AutoTikTokUploader** library. The function is designed to automate the process of uploading or scheduling videos to TikTok with additional features such as adding TikTok sounds, hashtags, and conducting copyright checks.

### ❗ Key Sections:

- **Parameter Explanations**: Provides detailed descriptions of each parameter, including the valid options and their effects.
- **Initialization Info**: Details instances that occur during first run of function
- **Important Notes**: Highlights important account recommendations and limitations related to TikTok accounts and scheduling.
- **Supported Captchas**: Showcases the Captchas the code is able to solve
- **Runtime**: Provides an estimate of how much runtime is added by different parameters
- **Example Usage**: Demonstrates a practical example of how to use the function.

## 📜 Function: `upload_tiktok`

### Parameters

- **`video`** (str)
  - The input path for your video file that you want to upload to TikTok.
  
- **`description`** (str)
  - The description text that will accompany the video when uploaded. hashtags included in description will NOT work, must be included in `hashtags` parameter

- **`hashtags`** (list of str, optional, default: None)
  - An array of hashtag strings (e.g., `['#example', '#fun']`) to be added to the video description.

- **`sound_name`** (str, optional, default: None)
  - The name of the TikTok sound that you want to use for the video. This sound will be applied during the upload.
  - NOTE: please be specific with sound name (include sound creator name also if possible)

- **`sound_aud_vol`** (str, optional, default: `'mix'`)
  - Determines the volume mix between the TikTok sound and the original video audio. Accepts one of the following options:
    - `'mix'`: The TikTok sound and original audio will have a 50/50 split.
    - `'background'`: The original audio will be louder, and the TikTok sound will be faintly heard in the background.
    - `'main'`: The TikTok sound will be louder, and the original audio will be faintly heard in the background.
  - Defaults to `'mix'` if invalid option chosen

- **`schedule`** (str, optional, default: None)
  - The time you want the video to be uploaded. The format should be `HH:MM`, and the minute (`MM`) must be a multiple of 5. The scheduled time must be at least 15 minutes later than the current local time (unless scheduling for a different day). The time should be in your local time zone.

- **`day`** (int, optional, default: None) (requires `schedule` != None)
  - If you want to schedule the video for a different day, this parameter specifies the day of the current month on which to upload the video. i.e: If current day is Sept 3rd, day=5 will upload video on Sept 5th
  - NOTE: You will also need to specify time of upload in `schedule` parameter or else `day` won't work

    **Important**:
    - You can only schedule a maximum of 10 days in advance.
    - If scheduling for the next month, you can only schedule within the first 5 days of the next month (as long as they are also within 10 days of the current date). i.e: If current day is Sept 30th, day=5 will upload on Oct 5th, 6 WILL NOT WORK.

- **`copyrightcheck`** (bool, optional, default: `False`)
  - If set to `True`, the function will conduct a copyright check on TikTok before uploading. If the check fails, the code execution will stop.

- **`suppressprint`** (bool, optional, default: `False`)
  - Suppresses print messages that indicate the progress of the video upload. It is recommended to set this to `False` when first running the code to see progress and ensure everything works correctly.


## 🛠️ Initialization Info

- **During FIRST RUN:** 

  - You will be asked to log-in to TikTok, your cookies from your log-in will then be stored in a file `TK_cookes.json`. If you wish to change the account you want to post to, just delete the cookies file and you will be prompted to log in again.

  - Javascript dependencies will be automatically downloaded, once downloaded it will not attempt to download it again unless the files get deleted.
  
  - Runtime might be a 20-30 seconds longer than usual, this is due to libraries being built. Runtime should return to normal after first run


## 📝 Important Notes

- **VERY IMPORTANT: TikTok Account Recommendations**:
  - It is recommended to have a TikTok account with at least a few weeks of history built up for the best results.
  - If you want to upload your video with TikTok sounds, your TikTok account MUST have the ability to save drafts; otherwise, you can just upload/schedule the video with copyright checks and trending hashtags.

- **Scheduling Limitations**:
  - The function allows scheduling up to 10 days in advance.
  - If you need to schedule a video for the next month, the video can only be uploaded within the first 5 days of that month (as long as these days are within 10 days from the current date).

## ⛔ Supported Captchas:

### Captcha solver currently supports Captchas of type:
<p align="center">
  <img src="READMEimage/Captcha1.gif" alt="" width="250" loop=infinite/>
</p>

<p align="center">
  <img src="READMEimage/2ndCaptcha.gif" alt="" width="250" loop=infinite/>
</p>

#### Note: 
- These GIFs are just to showcase the project's ability to auto-solve captcha's, this entire process will take place 'under the hood', you will not see the captcha being solved.

- As far as I'm aware these captchas are the only types of captchas that you may encounter when trying to upload TikTok's, if you do encounter a different captcha, I highly encourage you to email me and let me know and I will try to increase the capabilities of this project to include those captcha's as well.

- To check what captcha shows up when you upload on your account just open this link while logged in to TikTok: https://www.tiktok.com/tiktokstudio/upload?from=upload&lang=en

## 🕰️ Runtime:
**Total runtime depends on how long TikTok takes to upload your video to their servers, however, here are approximations on how much runtime is added by each parameter**

- **Captcha's:** 3 - 5 secs (during first run or in RARE cases, it can take 10-15 seconds longer)
- **Adding Sound:** 5 - 10 secs
- **Scheduling:** 1 - 3 secs
- **Copyright Check:** 2 - 7 secs

- **NOTE:** When running for the FIRST TIME ONLY, it may take an extra 20 - 30 seconds at the beginning for the code to start running as libraries are being built


## Example Usage

Here’s a basic example of how to use the `upload_tiktok` function:

```python
from autotiktokuploader import upload_tiktok

upload_tiktok(
    video='path/to/your/video.mp4',
    description='Check out my latest video!',
    hashtags=['#fun', '#viral'],
    sound_name='popular_sound',
    sound_aud_vol='mix',
    schedule='15:00',
    day=5,
    copyrightcheck=True,
    suppressprint=False
)
```

For more details or if errors persist, please feel free to contact me at haziqmk123@gmail.com or on LinkedIn (on my github profile)
