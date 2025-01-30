import sys
import subprocess
import json
import os
import time
from pypresence import Presence
from datetime import datetime, timedelta
import traceback

# Get CLIENT_ID from client-id.txt
if not os.path.exists("client-id.txt"):
    exit("Please make a client-id.txt file and put your discord client id in it.\nInstructions on how to do it: https://support-dev.discord.com/hc/en-us/articles/21204493235991-How-Can-Users-Discover-and-Play-My-Activity#h_01J8JK19X28EMARCNKRGW7J579")
with open("client-id.txt", "r") as f:
    CLIENT_ID = f.read().strip()

RPC = None
HOOK_SCRIPT = "/tmp/cmus_discord_presence.pid"

def get_cmus_status():
    """Get current CMUS status."""
    try:
        args = json.loads(sys.argv[1])
        args = dict(zip(args[0::2],args[1::2]))
        print(f"{args=}")
        args["position"] = int(subprocess.run("cmus-remote -Q | grep position | awk '{print $2}'", shell=True, capture_output=True, text=True).stdout.strip())
        return args
    except Exception:
        print(f"Error getting CMUS status: {traceback.format_exc()}")
        return None


def update_presence():
    """Update Discord presence."""
    global RPC

    status = get_cmus_status()
    print(status)
    if not status or status.get("status") == "stopped":
        RPC.clear()
        print("No music playing or stopped.")
        return

    title = f"{status.get('title', 'Unknown Title')}"
    artist = f"{status.get('artist', 'Unknown Artist')}"

    print("{} - {}".format(artist, title))
    position = status["position"]

    now = datetime.now()
    start_time = now - timedelta(seconds=position)

    RPC.update(
        details=title,
        state=artist,
        large_image="listen-moe",
        large_text="https://listen.moe/",
        small_image="github",
        small_text="github.com/Parsa-GP/cmus-rpc",
        start=int(start_time.timestamp()),

    )

try:
    print("Initializing Discord RPC...")
    RPC = Presence(CLIENT_ID)
    RPC.connect()

    # Update once at startup
    update_presence()

    # Wait for cmus hook trigger (using SIGUSR1)
    while True:
        time.sleep(999999)  # Just idle until interrupted

except KeyboardInterrupt:
    print("Exiting.")

except Exception as e:
    print(f"Error: {e}")

finally:
    if RPC:
        RPC.clear()
        RPC.close()
