# Telegram Automation

This section of the repository contains a standalone script, `Fancy_Upload.py`, which extends the functionality of the `tiktokautouploader` library. The script integrates additional automation features, particularly designed for Telegram-based control. **Please note that `Fancy_Upload.py` is not part of the main `tiktokautouploader` library.**

Code written by: t3k-vtx

## Features

The `Fancy_Upload.py` script provides the following functionalities:

1. **Folder Uploads:**
   - Uploads videos from a designated folder to TikTok in ascending order based on file names.

2. **Integration with Telegram Bot:**
   - Command-based status updates via `/status` or `/stats`.
   - Timer skipping functionality with the `/skip` command.
   - Notifications for errors or upload status updates sent to a Telegram group.

3. **Randomized Timer Intervals:**
   - Ensures uploads occur at randomized intervals between 6 to 9 hours to avoid TikTok rate limits.

4. **Post-Upload Management:**
   - Moves successfully uploaded videos to a separate folder to keep the upload folder organized.
   
## How to Use

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/TikTokAutoUploader.git
   ```

2. **Navigate to the `TelegramAutomation` Folder:**
   ```bash
   cd TelegramAutomation
   ```

3. **Install Dependencies:**
   - Ensure you have the `tiktokautouploader` library installed.
   - Install any additional libraries listed in the `Fancy_Upload.py` script.

4. **Configure Telegram Bot:**
   - Set up a Telegram bot and obtain the bot token.
   - Update the `Fancy_Upload.py` script with your Telegram bot token and group chat ID.

5. **Run the Script:**
   ```bash
   python Fancy_Upload.py
   ```

## Important Notes

- **Standalone Script:** `Fancy_Upload.py` is not integrated into the `tiktokautouploader` library. It is a standalone script that utilizes the library's features.
- **Customization Required:** Some configurations, such as folder paths and Telegram bot credentials, need to be updated in the script to match your setup.
- **Community Contribution:** This script was contributed by a community member (t3k-vtx) and is provided as-is. For issues or suggestions, please raise an issue in the repository.

## Contact

For further assistance, feel free to reach out via the repository's Issues section or contact t3k-vtx directly.

