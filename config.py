import json
from os import path

config = {}

class Config:
	def __init__(self, filepath:str="~/.config/music-rpc/config.jsonc"):
		if not path.exists(filepath):
			raise FileNotFoundError("The config file is nowhere to be found.\npath: "+filepath)
		with open(filepath) as f:
			self.data = json.load(f)

	def get(self, key, player:str):
		return self.data["server"][player].get(key)

	def getglobal(self, key, ):
		return self.data["server"].get(key)

