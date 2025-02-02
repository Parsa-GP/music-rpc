from os import path
from pypresence import Presence
from pypresence import exceptions as pyp_exceptions
from datetime import datetime, timedelta
from socket_handling import Server
from json import loads
from time import sleep
from traceback import format_exc
import configparser
import shutil

config = configparser.ConfigParser()
config_path = "~/.config/music-rpc/server.ini"

if not path.exists(config_path):
	shutil.copyfile("./server.ini", config_path)


def update_presence(status: str):
	"""Updates Discord presence."""
	global RPC
	global conf

	status = loads(status)

	if not status:
		print("No music playing")
		return

	print(status)
	match status["type"]:
		case "cmus":
			
			details = f"{status.get('title')}"
			state = f"{status.get('artist')}"

			if (details.strip() and state.strip()) or conf["DEFAULT"]["use_filename_if_empty"]:
				details_fmt = path.split(status["file"])[1]
				state_fmt = ""
			else:
				details_fmt = 'Unknown Title' if details=="" else details
				state_fmt = 'Unknown Artist' if state=="" else state

			now = datetime.now()
			start_time = None

			if conf["DEFAULT"]["send_song_start"]:
				start_time = int(now - timedelta(seconds=status["position"]).timestamp())
			if conf["DEFAULT"]["echo_playing"]:
				print("{} - {}".format(state_fmt, details_fmt))

			if status.get("status") == "paused":
				if conf["DEFAULT"]["clear_when_pause"]:
					RPC.clear()
				else:
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
					start=start_time,
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

def main():
	
	conf = config.read(config_path)
	RPC = None

	try:
		print("Initializing Discord RPC... ", end="")
		try:
			RPC = Presence(conf["DEFAULT"]["client_id"])
			RPC.connect()
		except pyp_exceptions.InvalidID:
			print("Client ID is Invalid.\nMake sure you copied it right or there's no junk in `client_id.txt`.")
			exit()
		print("OK")

		server = Server(port=conf["DEFAULT"]["port"])
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
