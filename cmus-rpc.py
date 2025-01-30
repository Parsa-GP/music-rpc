import sys
import subprocess
import json
import traceback
import socket_handling as sh

def get_cmus_status() -> dict:
	"""Get current CMUS status."""
	try:
		args = json.loads(sys.argv[1])
		args = dict(zip(args[0::2], args[1::2]))
		print(f"{args=}")
		args["position"] = int(subprocess.run("cmus-remote -Q | grep position | awk '{print $2}'", shell=True, capture_output=True, text=True).stdout.strip())
		return args
	except Exception:
		print(f"Error getting CMUS status: {traceback.format_exc()}")
		return None

def main():
	client = sh.Client(port=6473)
	client.connect()
	client.send(json.dumps(get_cmus_status()))
	client.close()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Exiting.")

