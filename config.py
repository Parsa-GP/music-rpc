import json

config = {}

class Config:
	def __init__(self, filepath:str="config.jsonc"):
		with open(filepath) as f:
			self.data = json.load(f)

# i should make template or some sort
# the code repeating isn't efficient

class Server:
	def __init__(self, conf:Config, player:str):
		self.config = conf
		self.data = conf.data["server"]
		self.player = player

	def get(self, key):
		return self.data[self.player].get(key)

	def getglobal(self, key):
		return self.data.get(key)


class Client:
	def __init__(self, conf:Config, player:str):
		self.config = conf
		self.data = conf.data["client"]
		self.player = player

	def get(self, key):
		return self.data[self.player].get(key)

	def getglobal(self, key):
		return self.data.get(key)
