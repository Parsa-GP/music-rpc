import os
from pypresence import Presence
from pypresence import exceptions as pyp_exceptions
from datetime import datetime, timedelta
import socket_handling as sh
import json
from time import sleep

# Get CLIENT_ID from client-id.txt
if not os.path.exists("client-id.txt"):
	exit("Please make a client-id.txt file and put your discord client id in it.\nInstructions on how to do it: https://support-dev.discord.com/hc/en-us/articles/21204493235991-How-Can-Users-Discover-and-Play-My-Activity#h_01J8JK19X28EMARCNKRGW7J579")
with open("client-id.txt", "r") as f:
	CLIENT_ID = f.read().strip()

RPC = None

def update_presence(status):
	"""Update Discord presence."""
	global RPC

	status = json.loads(status)

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
	print("Initializing Discord RPC... ", end="")
	try:
		RPC = Presence(CLIENT_ID)
		RPC.connect()
	except pyp_exceptions.InvalidID:
		print("Client ID is Invalid.\nMake sure you copied it right or there's no junk in `client_id.txt`.")
		exit()
	print("OK")

	server = sh.Server(port=6473)
	while True:
		server.start(update_presence)
		print("Waiting 10s to reconnect")
		sleep(10)

except KeyboardInterrupt:
	print("Exiting.")
except Exception as e:
	print(f"Error: {e} ({type(e)})")
finally:
	if RPC:
		try:
			RPC.clear()
			RPC.close()
		except ConnectionResetError:
			print("Connection reset.\nmake sure discord is opened or the app is not blocked by the firewall.")
		except pyp_exceptions.PipeClosed:
			print("The pipe was closed.\nmake sure discord is opened or the app is not blocked by the firewall.")
