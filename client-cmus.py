import sys
import subprocess
import json
import traceback
import socket_handling as sh

def get_status() -> dict:
	"""Get current CMUS status."""
	try:
		args = json.loads(sys.argv[1])
		args = dict(zip(args[0::2], args[1::2]))
		args["type"] = "cmus"
		args["position"] = int(subprocess.run("cmus-remote -Q | grep position | awk '{print $2}'", shell=True, capture_output=True, text=True).stdout.strip())
		return args
	except Exception:
		print(f"Error getting CMUS status: {traceback.format_exc()}")
		return None

def main():
	client = sh.Client(port=6473)
	client.connect()
	status = json.dumps(get_status())
	print(f"Sent: {status}")
	client.send(status)
	client.close()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Exiting.")

