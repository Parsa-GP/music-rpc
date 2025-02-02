from os import path, getcwd
from pypresence import Presence
from pypresence import exceptions as pyp_exceptions
from datetime import datetime, timedelta
from socket_handling import Server
from json import loads
from time import sleep
from traceback import format_exc

# Get CLIENT_ID from client-id.txt
if not path.exists("client-id.txt"):
	exit(f"Please make a client-id.txt file and put your discord client id in it.\nWe are in: {getcwd()}\nInstructions on how to do it: https://support-dev.discord.com/hc/en-us/articles/21204493235991-How-Can-Users-Discover-and-Play-My-Activity#h_01J8JK19X28EMARCNKRGW7J579")
with open("client-id.txt", "r") as f:
	CLIENT_ID = f.read().strip()

RPC = None

def update_presence(status: str):
	"""Updates Discord presence."""
	global RPC

	status = loads(status)

	if not status:
		print("No music playing")
		return

	print(status)
	match status["type"]:
		case "cmus":
			details = f"{status.get('title')}"
			state = f"{status.get('artist')}"
			if details.strip() and state.strip():
				
				details_fmt = path.split(status["file"])[1]
				state_fmt = "  "
			else:
				details_fmt = 'Unknown Title' if details=="" else details
				state_fmt = 'Unknown Artist' if state=="" else state


			now = datetime.now()
			start_time = now - timedelta(seconds=status["position"])
			
			print("{} - {}".format(state_fmt, details_fmt))
			if status.get("status") == "paused":
				#RPC.clear()
				RPC.update(
					details=f"{details_fmt:2}",
					state=f"{state_fmt:2}",
					large_image="music-miku-heart-pause",
					large_text="MIKU NOOOO",
					small_image="github",
					small_text="Parsa-GP/music-rpc",
				)
				print("Music stopped.")
			else: 
				RPC.update(
					details=f"{details_fmt:2}",
					state=f"{state_fmt:2}",
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

	server = Server(port=6473)
	while True:
		try:
			server.start(update_presence)
		except pyp_exceptions.PipeClosed as e:
			print(format_exc())
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
