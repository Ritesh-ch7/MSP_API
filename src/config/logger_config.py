import os, zipfile, uuid, logging
from logging.handlers import TimedRotatingFileHandler
from fastapi.logger import logger

logger.setLevel(logging.INFO)
fileHandler = TimedRotatingFileHandler("src/logging/app.log", backupCount=10, when='midnight', interval=1)
fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
fileHandler.namer = lambda name : name.replace("app.log", "") + '.log'
logger.addHandler(fileHandler)
new_logger = logger



