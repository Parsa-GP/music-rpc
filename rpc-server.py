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
import log

log = log.Log("rpc_server.log", echo=True)

config = configparser.ConfigParser()
config_path = path.expanduser("~/.config/music-rpc/server.ini")
config.read(config_path)

if not path.exists(config_path):
	shutil.copy("server.ini", config_path)

def update_presence(status: str, RPC):
	"""Updates Discord presence."""
	global config

	status = loads(status)

	if not status:
		log.info("No music playing", echo=True)
		return

	log.debug(f"{status=}")
	match status["type"]:
		case "cmus":
			
			details = f"{status.get('title')}"
			state = f"{status.get('artist')}"

			if (details.strip() and state.strip()) or config.getboolean("cmus", "use_filename_if_empty"):
				details_fmt = path.split(status["file"])[1]
				state_fmt = ""
			else:
				details_fmt = 'Unknown Title' if details=="" else details
				state_fmt = 'Unknown Artist' if state=="" else state

			now = datetime.now()
			start_time = None

			if config.getboolean("cmus", "send_song_start"):
				start_time = int((now - timedelta(seconds=status["position"])).timestamp())
			if config.getboolean("DEFAULT", "echo_playing"):
				print("{} - {}".format(state_fmt, details_fmt))

			if status.get("status") == "paused":
				log.debug("paused")
				if config.getboolean("cmus", "clear_when_pause"):
					log.debug("clear_when_pause=True")
					RPC.clear()
				else:
					log.debug("clear_when_pause=False")
					RPC.update(
						details=f"{details_fmt:2}",
						state=f"{state_fmt:2}",
						large_image="music-miku-heart-pause",
						large_text="MIKU NOOOO",
						small_image="github",
						small_text="Parsa-GP/music-rpc",
					)
				log.info("Music stopped.", echo=True)
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

			log.info("{} - {}".format(artists, title) if artists else title, echo=True)

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
			log.info("tf is this shi\n bro doin "+status["type"], echo=True)

def main():
	
	config.read(config_path)

	try:
		log.info("Initializing Discord RPC...")
		try:
			RPC = Presence(config.getint("DEFAULT", "client_id"))
			RPC.connect()
		except pyp_exceptions.InvalidID:
			log.error("Client ID is Invalid.")
			exit()
		log.info("Initialized Discord RPC")

		server = Server(port=config.getint("DEFAULT", "port"))
		while True:
			try:
				server.start(update_presence, RPC)
			except pyp_exceptions.PipeClosed:
				log.error(format_exc())
				log.info("Waiting 10s to reconnect", echo=True)
				sleep(10)
			except ConnectionResetError:
				log.error("Connection reset.\nmake sure discord is opened or the app is not blocked by the firewall.")
				exit()

	except KeyboardInterrupt:
		log.info("Exiting with ^C")
		if RPC:
			try:
				RPC.clear()
				RPC.close()
			except pyp_exceptions.PipeClosed:
				log.error("The pipe was closed.\nmake sure discord is opened or the app is not blocked by the firewall.")
				exit()
if __name__ == "__main__":
	main()
