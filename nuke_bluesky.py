from atproto import Client
import time

BSKY_HANDLE = 'your_bsky_handle_here' # Replace with your actual Bluesky handle
BSKY_APP_PASSWORD = 'your_pw_here' # Replace with your actual Bluesky app password

CALL_DELAY = 0.5
RETRY_DELAY = 5

def safe_api_call(func, *args, **kwargs):
    retries = 3
    for attempt in range(retries):
        try:
            result = func(*args, **kwargs)
            time.sleep(CALL_DELAY)
            return result
        except Exception as e:
            print(f"API error: {e}. Retrying in {RETRY_DELAY} seconds... (Attempt {attempt+1}/{retries})")
            time.sleep(RETRY_DELAY)
    print(f"Failed after {retries} retries. Skipping.")
    return None

def nuke_bluesky():
    client = Client()
    client.login(BSKY_HANDLE, BSKY_APP_PASSWORD)
    my_did = client.me.did
    print(f"Logged in as: {my_did}")

    # Delete own posts (including replies and media)
    print("Deleting posts, replies, and media...")
    cursor = None
    while True:
        records = safe_api_call(client.com.atproto.repo.list_records, {
            'repo': my_did,
            'collection': 'app.bsky.feed.post',
            'limit': 100,
            'cursor': cursor
        })
        if not records or not records.records:
            break
        for record in records.records:
            rkey = record.uri.split('/')[-1]
            print(f"Deleting post: {rkey}")
            safe_api_call(client.com.atproto.repo.delete_record, {
                'repo': my_did,
                'collection': 'app.bsky.feed.post',
                'rkey': rkey
            })
        cursor = records.cursor

    # Delete reposts (reskeets)
    print("Deleting reposts (reskeets)...")
    cursor = None
    while True:
        reposts = safe_api_call(client.com.atproto.repo.list_records, {
            'repo': my_did,
            'collection': 'app.bsky.feed.repost',
            'limit': 100,
            'cursor': cursor
        })
        if not reposts or not reposts.records:
            break
        for repost in reposts.records:
            rkey = repost.uri.split('/')[-1]
            subject = repost.value['subject']
            print(f"Deleting repost of: {subject['uri']}")
            safe_api_call(client.com.atproto.repo.delete_record, {
                'repo': my_did,
                'collection': 'app.bsky.feed.repost',
                'rkey': rkey
            })
        cursor = reposts.cursor

    # Delete likes (currently not supported)
    print("Bluesky doesn't offer an official API to list your likes for mass deletion yet.")
    print("Consider manually unliking specific posts in the app.")

    # Unfollow everyone (deleting follow records)
    print("Unfollowing everyone...")
    cursor = None
    while True:
        follows = safe_api_call(client.com.atproto.repo.list_records, {
            'repo': my_did,
            'collection': 'app.bsky.graph.follow',
            'limit': 100,
            'cursor': cursor
        })
        if not follows or not follows.records:
            break
        for record in follows.records:
            rkey = record.uri.split('/')[-1]
            subject_did = record.value['subject']
            print(f"Unfollowing: {subject_did}")
            safe_api_call(client.com.atproto.repo.delete_record, {
                'repo': my_did,
                'collection': 'app.bsky.graph.follow',
                'rkey': rkey
            })
        cursor = follows.cursor

    print("🔥 All your posts, reposts, follows, and media have been nuked. 🔥")

if __name__ == "__main__":
    nuke_bluesky()
