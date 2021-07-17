from datetime import datetime

import websocket
import json
import config
import time
import math
import atexit

from binance.enums import *
from binance.client import Client
from utils import write, create_socket_string



SOCKET = create_socket_string()

client = Client(config.API_KEY, config.API_SECRET)

def exit_handler():
    write("Closing program...")


def on_message(_, message):
    pass


def on_open(_):
    write('opened connection')


def on_close(_):
    write('closed connection')


atexit.register(exit_handler)
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()
