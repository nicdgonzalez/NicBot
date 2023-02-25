import datetime
import logging
import os

from nicbot import NicBot

os.mkdir("./logs") if not os.path.exists("./logs") else None

logging.basicConfig(
    filename='./logs/%s.log' % (datetime.datetime.now().date()),
    filemode='w+',
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%m-%d-%Y %H:%M:%S',
    level=logging.DEBUG
)

if __name__ == "__main__":
    NicBot().run()
