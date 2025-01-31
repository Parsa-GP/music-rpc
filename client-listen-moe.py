import asyncio
import json
from mpv import MPV
import socket_handling as sh
import websockets
import datetime
from zoneinfo import ZoneInfo
from os import getlogin, path

# Get CLIENT_ID from client-id.txt
if not path.exists("client-id.txt"):
	exit("Please make a client-id.txt file and put your discord client id in it.\n Instructions on how to do it: https://support-dev.discord.com/hc/en-us/articles/21204493235991-How-Can-Users-Discover-and-Play-My-Activity#h_01J8JK19X28EMARCNKRGW7J579")
with open("client-id.txt", "r") as f:
	DISCORD_CLIENT_ID = f.read()

# Constants
LISTEN_MOE_STREAM_URL = "https://listen.moe/stream"
WEBSOCKET_URL = "wss://listen.moe/gateway_v2"

async def send_ws(ws, data):
	"""Send data through the WebSocket."""
	json_data = json.dumps(data)
	await ws.send(json_data)

async def _send_pings(ws, interval=45):
	"""Send periodic pings to keep the WebSocket connection alive."""
	while True:
		await asyncio.sleep(interval)
		msg = {'op': 9}
		await send_ws(ws, msg)

async def fetch_song_info():
	"""Fetch song info via WebSocket and update Discord RPC."""
	player = MPV()
	player.play(LISTEN_MOE_STREAM_URL)
	
	async with websockets.connect(WEBSOCKET_URL) as ws:
		while True:
			data = json.loads(await ws.recv())
			
			if data['op'] == 0:  # Hello packet
				heartbeat = data['d']['heartbeat'] / 1000
				asyncio.create_task(_send_pings(ws, heartbeat))
			elif data['op'] == 1:  # Event packet
				song_data = data['d']
				send_data = {"type":"listen-moe"}
				song = song_data.get('song', {})
				send_data["title"] = song.get('title', "Unknown")
				send_data["artists"] = ", ".join(artist.get("name") for artist in song.get('artists', []))
				start = datetime.datetime.strptime(song_data["startTime"], '%Y-%m-%dT%H:%M:%S.%fZ')
				start = int(start.replace(tzinfo=ZoneInfo("UTC")).timestamp())
				send_data["start"] = start
				print(f"{send_data["title"]} by {send_data["artists"]}")

				client = sh.Client(port=6473)
				client.connect()
				print(send_data)
				client.send(json.dumps(send_data))
				client.close()


async def main():
	try:
		await fetch_song_info()
	except KeyboardInterrupt:
		print("Stopping the music...")

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print(f"Have a good day, {getlogin()}-san!")
