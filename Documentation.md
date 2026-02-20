# tiktokautouploader Documentation

This document provides detailed information about the parameters and usage of the `upload_tiktok` function in the **tiktokautouploader** library. The function is designed to automate the process of uploading or scheduling videos to TikTok with additional features such as adding TikTok sounds, hashtags, and conducting copyright checks.

### Key Sections:

- **Parameter Explanations**: Provides detailed descriptions of each parameter, including the valid options and their effects.
- **Initialization Info**: Details instances that occur during first run of function
- **Important Notes**: Highlights important account recommendations and limitations related to TikTok accounts and scheduling.
- **Supported Captchas**: Showcases the Captchas the code is able to solve
- **Runtime**: Provides an estimate of how much runtime is added by different parameters
- **Example Usage**: Demonstrates a practical example of how to use the function.

## Function: `upload_tiktok`

### Parameters

- **`video`** (str)
  - The input path for your video file that you want to upload to TikTok.
  
- **`description`** (str)
  - The description text that will accompany the video when uploaded. hashtags included in description will NOT work, must be included in `hashtags` parameter

- **`accountname`** (str)
   - The name of the account you want to post on.
     
   - **NOTE:** When uploading to an account for the FIRST TIME ONLY, you will be prompted to log-in, once you log-in your cookies will be stored and you will not need to log-in to that account again. Read INITIALIZATION section for more info.

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
    - You can only schedule a maximum of 240 hours (10 days) in advance.
    - If scheduling for the next month, you can only schedule within the first 2 days of the next month (as long as they are also within 10 days of the current date). i.e: If current day is Sept 30th, day=2 will upload on Oct 2nd, 4 WILL NOT WORK.

- **`copyrightcheck`** (bool, optional, default: `False`)
  - If set to `True`, the function will conduct a copyright check on TikTok before uploading. If the check fails, the code execution will stop.
  
- **`stealth`** (bool, optional, default: `False`)
  - If set to `True`, the function will wait a couple of seconds between each operation to make it harder for TikTok to detect automation use.

- **`suppressprint`** (bool, optional, default: `False`)
  - Suppresses print messages that indicate the progress of the video upload. It is recommended to set this to `False` when first running the code to see progress and ensure everything works correctly.

- **`headless`** (bool, optional, default: True)
  - Runs the code in headless mode, when set to `False` you can see the code execute in the browser, recommended to set this to `False` if code is not working as intended in order to more clearly see what the issue exactly is

- **`proxy`** (dict, optional, default: None)
  - Allows user to run the code on a proxy server
  - Must be a dictionary with "server" key that has a string of proxy server IP address
  - Optionally can also include "username" and "password" keys for authentication
  - feature was contributed by KryvMykyta

- **`search_mode`** (str, optional, default: `'search'`)
  - Determines how the function looks up the sound specified in `sound_name`. Accepts one of the following options:
    - `'search'`: Searches TikTok for the sound by name. This is the default behaviour.
    - `'favorites'`: Looks for the sound in your TikTok account's saved favorites instead of searching.
      
  - NOTE: `sound_name` must be provided for this parameter to have any effect. If using `'favorites'`, make sure the sound is actually saved to your account beforehand.


## Initialization Info

- **During FIRST RUN:**

  - Javascript dependencies will be automatically downloaded, once downloaded it will not attempt to download it again unless the files get deleted.
  
  - Runtime might be a 20-30 seconds longer than usual, this is due to libraries being built. Runtime should return to normal after first run

- **When uploading to an account for the FIRST TIME:**

  - You will be asked to log-in to TikTok, your cookies from your log-in will then be stored in a file called `TK_cookies_(youraccountname).json`. You will not need to log-in to that account again after that.


## Important Notes

**VERY IMPORTANT: Use this tool at your own risk, as automated uploading may violate TikTok's Terms of Service** 

- **TikTok Account Recommendations**:
  - It is recommended to have a TikTok account with at least a few weeks of history built up for the best results.

- **Scheduling Limitations**:
  - The function allows scheduling up to 240 hours (10 days) in advance.
  - If you need to schedule a video for the next month, the video can only be uploaded within the first 2 days of that month (as long as these days are also within 10 days from the current date).

## Supported Captchas:

### Captcha solver currently supports Captchas of type:
<p align="center">
  <img src="READMEimage/Captcha1.gif" alt="" width="250" loop=infinite/>
</p>

<p align="center">
  <img src="READMEimage/2ndCaptcha.gif" alt="" width="250" loop=infinite/>
</p>

#### Note: 
- These GIFs are just to showcase the project's ability to auto-solve captcha's, this entire process will take place 'under the hood' (unless headless mode is set to `False`).

## Runtime:
**Total runtime mostly depends on your WIFI connection, however, here are approximations on how much runtime is added by each parameter**

- **Captcha's:** 3 - 10 secs
- **Adding Sound:** 3 - 5 secs (```stealth=True``` adds around 8 seconds)
- **Scheduling:** 2 - 3 secs (```stealth=True``` adds around 6 seconds)
- **Copyright Check:** 2 - 5 secs (```stealth=True``` adds around 2 seconds)

- All in all, runtime won't exceed 20 seconds in most cases (unless ```stealth=True```).

- **NOTE:** When running for the FIRST TIME ONLY, it may take an extra 20 - 30 seconds at the beginning for the code to start running as JS libraries are being built


## Example Usage

Here's a basic example of how to use the `upload_tiktok` function:

```python
from tiktokautouploader import upload_tiktok

upload_tiktok(
    video='path/to/your/video.mp4',
    description='Check out my latest video!',
    accountname= 'mytiktokaccount',
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
