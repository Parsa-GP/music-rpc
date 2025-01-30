import sys
sys.argv.append("END")
open("/tmp/rpc-test","w").write("open\n")
open("/tmp/rpc-test","a").write(" , ".join(sys.argv))
open("/tmp/rpc-test","a").write("\nsuccess")
exit()
import os
import psutil
import time
from pypresence import Presence
import subprocess
from datetime import datetime, timedelta
import re

# Get CLIENT_ID from client-id.txt
if not os.path.exists("client-id.txt"):
    exit("Please make a client-id.txt file and put your discord client id in it.\n Instructions on how to do it: https://support-dev.discord.com/hc/en-us/articles/21204493235991-How-Can-Users-Discover-and-Play-My-Activity#h_01J8JK19X28EMARCNKRGW7J579")
with open("client-id.txt", "r") as f:
    CLIENT_ID = f.read().strip()

RPC = None
HOOK_SCRIPT = "/tmp/cmus_discord_presence.pid"


def kill_existing_instance():
    """Kill any existing instance of this script."""
    current_pid = os.getpid()
    if os.path.exists(HOOK_SCRIPT):
        try:
            with open(HOOK_SCRIPT, "r") as pid_file:
                existing_pid = int(pid_file.read().strip())
            # Kill the existing process
            if psutil.pid_exists(existing_pid) and existing_pid != current_pid:
                psutil.Process(existing_pid).terminate()
                print(f"Terminated previous instance: {existing_pid}")
        except (ValueError, psutil.NoSuchProcess):
            pass

    # Write the current PID to the file
    with open(HOOK_SCRIPT, "w") as pid_file:
        pid_file.write(str(current_pid))

def get_cmus_status():
    """Get current CMUS status."""
    try:
        # Input string
        input_string = sys.argv

        # Regular expression to match the desired parts
        pattern = r"status (\w+) file ([^\s]+) artist ([^\s]+) albumartist ([^\s]+) album ([^\s]+) tracknumber (\d+) title ([^\s]+)"

        # Apply the regex pattern
        match = re.search(pattern, input_string)

        # Create a dictionary with the matched data
        if match:
            result = {
                "status": match.group(1),
                "file": match.group(2),
                "artist": match.group(3),
                "album": match.group(5),
                "position": match.group(6),
                "title": match.group(7)
            }

            print(result)
        else:
            print("No match found")
    except Exception as e:
        print(f"Error getting CMUS status: {e}")
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
    position = int(status["position"])

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

kill_existing_instance()

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
