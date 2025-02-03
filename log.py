import logging
from sys import stdout

class Log:
	def __init__(self, filename:str, echo:bool=False):
		logging.basicConfig(filename=filename, level=logging.INFO, format="%(asctime)s [%(levelname)-4.4s] %(message)s")
		if echo:
			logging.getLogger().addHandler(logging.StreamHandler(stdout))
		self.log = logging.getLogger(__name__)

	def debug(self, msg, echo=False):
		self.log.debug(msg)
		if echo:
			print("[DBG ] "+msg)
	
	def info(self, msg, echo=False):
		self.log.info(msg)
		if echo:
			print("[INFO] "+msg)
	
	def warning(self, msg, echo=False):
		self.log.warning(msg)
		if echo:
			print("[WARN] "+msg)
	
	def error(self, msg, echo=False):
		self.log.error(msg)
		if echo:
			print("[ERR ] "+msg)
		print("Something went wrong. Check the logs")
	
	def critical(self, msg, echo=False):
		self.log.critical(msg)
		if echo:
			print("[CLIT] "+msg)
		print("Something SERIOUS went wrong. Check the logs")
