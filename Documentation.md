# autotiktokuploader Documentation

This document provides detailed information about the parameters and usage of the `upload_tiktok` function in the **AutoTikTokUploader** library. The function is designed to automate the process of uploading or scheduling videos to TikTok with additional features such as adding TikTok sounds, hashtags, and conducting copyright checks.

## 📜 Function: `upload_tiktok`

### Parameters

- **`video`** (str)
  - The input path for your video file that you want to upload to TikTok.
  
- **`description`** (str)
  - The description text that will accompany the video when uploaded.

- **`hashtags`** (list of str)
  - An array of hashtag strings (e.g., `['#example', '#fun']`) to be added to the video description.

- **`cookies_path`** (str)
  - The file path to your `cookies.json` file, which is used for authenticating your TikTok account.

- **`sound_name`** (str, optional, default: None)
  - The name of the TikTok sound that you want to use for the video. This sound will be applied during the upload. Defaults to None

- **`sound_aud_vol`** (str, optional, default: `'mix'`)
  - Determines the volume mix between the TikTok sound and the original video audio. Accepts one of the following options:
    - `'mix'`: The TikTok sound and original audio will have a 50/50 split.
    - `'background'`: The original audio will be louder, and the TikTok sound will be faintly heard in the background.
    - `'main'`: The TikTok sound will be louder, and the original audio will be faintly heard in the background.

- **`schedule`** (str, optional, default: None)
  - The time you want the video to be uploaded. The format should be `HH:MM`, and the minute (`MM`) must be a multiple of 5. The scheduled time must be at least 15 minutes later than the current local time (unless scheduling for a different day). The time should be in your local time zone.

- **`day`** (int, optional, default: None)
  - If you want to schedule the video for a different day, this parameter specifies the day of the current month on which to upload the video. i.e: If current day is Sept 3rd, day=5 will upload video on Sept 5th

    **Important**:
    - You can only schedule a maximum of 10 days in advance.
    - If scheduling for the next month, you can only schedule within the first 5 days of the next month (as long as they are also within 10 days of the current date). i.e: If current day is Sept 30th, day=5 will upload on Oct 5th, 6 WILL NOT WORK.

- **`copyrightcheck`** (bool, optional, default: `False`)
  - If set to `True`, the function will conduct a copyright check on TikTok before uploading. If the check fails, the video will be saved as a draft, and the code execution will stop.

- **`suppressprint`** (bool, optional, default: `True`)
  - Suppresses print messages that indicate the progress of the video upload. It is recommended to set this to `False` when first running the code to see progress and ensure everything works correctly.

### 📝 Other Notes

- **TikTok Account Recommendations**:
  - It is recommended to have a TikTok account with at least a few weeks of cookies built up for the best results.
  - Your TikTok account must have the ability to save drafts; otherwise, the code may not work correctly.

- **Scheduling Limitations**:
  - The function allows scheduling up to 10 days in advance.
  - If you need to schedule a video for the next month, the video can only be uploaded within the first 5 days of that month (as long as these days are within 10 days from the current date).

## Example Usage

Here’s a basic example of how to use the `upload_tiktok` function:

```python
from autotiktokuploader import upload_tiktok

upload_tiktok(
    video='path/to/your/video.mp4',
    description='Check out my latest video!',
    hashtags=['#fun', '#viral'],
    cookies_path='path/to/cookies.json',
    sound_name='popular_sound',
    sound_aud_vol='mix',
    schedule='15:00',
    day=5,
    copyrightcheck=True,
    suppressprint=False
)
```

For more details, please feel free to contact me at haziqmk123@gmail.com or on LinkedIn (on my github profile)

### Key Sections:

- **Parameter Explanations**: Provides detailed descriptions of each parameter, including the valid options and their effects.
- **Other Notes**: Highlights recommendations and limitations related to TikTok accounts and scheduling.
- **Example Usage**: Demonstrates a practical example of how to use the function.
