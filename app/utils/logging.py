import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger('transcript-intel')
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)