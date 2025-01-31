import os
from pypresence import Presence
from pypresence import exceptions as pyp_exceptions
from datetime import datetime, timedelta
import socket_handling as sh
import json
from time import sleep

# Get CLIENT_ID from client-id.txt
if not os.path.exists("client-id.txt"):
	exit(f"Please make a client-id.txt file and put your discord client id in it.\nWe are in: {os.getcwd()}\nInstructions on how to do it: https://support-dev.discord.com/hc/en-us/articles/21204493235991-How-Can-Users-Discover-and-Play-My-Activity#h_01J8JK19X28EMARCNKRGW7J579")
with open("client-id.txt", "r") as f:
	CLIENT_ID = f.read().strip()

RPC = None

def update_presence(status):
	"""Update Discord presence."""
	global RPC

	status = json.loads(status)

	if not status:
		print("No music playing")
		return

	#print(status)
	match status["type"]:
		case "cmus":

			title = f"{status.get('title', 'Unknown Title')}"
			artist = f"{status.get('artist', 'Unknown Artist')}"

			now = datetime.now()
			start_time = now - timedelta(seconds=status["position"])

			print("{} - {}".format(artist, title))
			if status.get("status") == "paused":
				#RPC.clear()
				RPC.update(
					details=f"{title:2}",
					state=f"{artist:2}",
					large_image="music-miku-heart-pause",
					large_text="MIKU NOOOO",
					small_image="github",
					small_text="Parsa-GP/music-rpc",
				)
				print("Music stopped.")
			else: 
				RPC.update(
					details=f"{title:2}",
					state=f"{artist:2}",
					large_image="music-miku-heart",
					large_text="MIKU",
					small_image="github",
					small_text="Parsa-GP/music-rpc",
					start=int(start_time.timestamp()),
				)
		case "listen-moe":
			title = f"{status.get('title', 'Unknown Title')}"
			artists = f"{status.get('artists', 'Unknown Artist')}"
			start = status["start"]

			print("{} - {}".format(artists, title) if artists else title)

			RPC.update(
				details=f"{title:2}",
				state=f"{artists:2}",
				large_image="listen-moe",
				large_text="https://listen.moe/",
				small_image="github",
				small_text="Parsa-GP/music-rpc",
				start=start,
			)
		case _:
			print("tf is this shi")

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
finally:
	if RPC:
		try:
			RPC.clear()
			RPC.close()
		except ConnectionResetError:
			print("Connection reset.\nmake sure discord is opened or the app is not blocked by the firewall.")
		except pyp_exceptions.PipeClosed:
			print("The pipe was closed.\nmake sure discord is opened or the app is not blocked by the firewall.")
