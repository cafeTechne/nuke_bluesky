# Bluesky Nuke Script

This Python script automates the deletion of your Bluesky account content, including posts, reposts (reskeets), media, and unfollows. It leverages the [atproto](https://github.com/MarshalX/atproto) library to interact with the Bluesky (AT Protocol) API.

## Features

- Deletes your Bluesky posts, including replies and media.
- Removes reposts (reskeets).
- Unfollows all accounts.
- Provides a retry mechanism for API calls.
- Graceful handling of API errors and delays to avoid rate limits.
- **Note:** The script does not yet support mass deletion of likes, as Bluesky's official API does not currently expose this functionality.

## Prerequisites

- Python 3.7+
- Install the `atproto` library:

`pip install atproto`

## Usage

1. **Clone this repository or copy the script.**
2. **Set your Bluesky credentials** in the script:
   - Replace `your_bsky_handle_here` with your actual Bluesky handle.
   - Replace `your_pw_here` with your Bluesky app password.
3. **Run the script**:
    ```bash
    python bluesky_nuke.py
    ```

The script will log into your Bluesky account and start deleting content.

## Configuration Options

- CALL_DELAY: Time in seconds to wait between API calls to avoid rate limits (default: 0.5).

- RETRY_DELAY: Time in seconds to wait before retrying failed API calls (default: 5).

These values can be adjusted at the top of the script.

## Warnings

This script permanently deletes your Bluesky posts, reposts, media, and unfollows. Use with caution.

The deletion of likes is not supported at this time due to API limitations.

Make sure to back up any content you wish to keep before running this script.

## Contribution

Feel free to submit pull requests or open issues for feature requests, bug reports, or improvements.

## License

This project is licensed under the MIT License.

