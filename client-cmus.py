from sys import argv
from subprocess import run
from json import loads, dumps
from traceback import format_exc
from socket_handling import Client

def get_status() -> dict:
	"""Get current CMUS status."""
	try:
		args = loads(argv[1])
		args = dict(zip(args[0::2], args[1::2]))
		args["type"] = "cmus"
		args["position"] = int(run("cmus-remote -Q | grep position | awk '{print $2}'", shell=True, capture_output=True, text=True).stdout.strip())
		return args
	except Exception:
		print(f"Error getting CMUS status: {format_exc()}")
		return None

def main():
	client = Client(port=6473)
	client.connect()
	status = dumps(get_status())
	print(f"Sent: {status}")
	client.send(status)
	client.close()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Exiting.")

