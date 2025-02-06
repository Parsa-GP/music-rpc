import logging
from sys import stdout

class CustomFormatter(logging.Formatter):
	def format(self, record):
		LEVEL_FORMAT_MAP = {
			"DEBUG": "DBUG",
			"INFO": "INFO",
			"WARNING": "WARN",
			"ERROR": "EROR",
			"CRITICAL": "CRIT"
		}
		record.levelname = LEVEL_FORMAT_MAP.get(record.levelname, record.levelname)
		return super().format(record)

class Log:
	def __init__(self, filename:str, echo:bool=False, level=logging.DEBUG):
		self.log = logging.getLogger(__name__)
		self.log.setLevel(level)  # Set the logging level

		# Create a formatter
		formatter = CustomFormatter("%(created).2f [%(levelname)-4.4s] %(message)s")

		# Create a file handler
		file_handler = logging.FileHandler(filename)
		file_handler.setFormatter(formatter)
		self.log.addHandler(file_handler)

		# Create a console handler (for terminal output)
		if echo:
			console_handler = logging.StreamHandler(stdout)
			console_handler.setFormatter(formatter)
			self.log.addHandler(console_handler)

	def debug(self, msg, echo=False):
		self.log.debug(msg)
		if echo:
			print("[DBUG] "+msg)
	
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
			print("[EROR] "+msg)
		print("Something went wrong. Check the logs")
	
	def critical(self, msg, echo=False):
		self.log.critical(msg)
		if echo:
			print("[CLIT] "+msg)
		print("Something SERIOUS went wrong. Check the logs")
