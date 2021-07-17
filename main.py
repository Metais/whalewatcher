import websocket
import json
import config
import time
import atexit

from binance.client import Client
from utils import write, create_socket_string, abort

SOCKET = create_socket_string()
WHALE_CUTOFF = 0.017  # % change in a minute candle that would describe a whale purchase/sell
MINIMUM_WHALE_FACTOR = 3.5  # minimum accepted ratio between upper wick and price change to be considered whale purchase

client = Client(config.API_KEY, config.API_SECRET)


def exit_handler():
    write("Closing program...")


def on_message(_, message):
    try:
        json_message = json.loads(message)

        # ignore if unclosed candle
        is_candle_closed = json_message['data']['k']['x']
        if not is_candle_closed:
            return

        # with this program, we're not interested in the 'lowest' price of a candle
        # amplitude is best measured as the ratio of highest price to opening price
        # basically, we don't care about 'bottom-wicks', since it could flag high amplitude for wrong reasons
        amplitude = (float(json_message['data']['k']['h']) - float(json_message['data']['k']['o'])) / \
                    float(json_message['data']['k']['o'])

        if amplitude > WHALE_CUTOFF:
            # for determining candle color
            price_change = float(json_message['data']['k']['c']) - float(json_message['data']['k']['o'])
            candle_color = "red" if price_change < 0 else "green" if price_change > 0 else "unchanged"

            # for determining chance that this was a whale (high number == high chance of whale)
            price_change_ratio = price_change / float(json_message['data']['k']['o'])
            if price_change_ratio < 0.001:
                whale_factor = 10
            else:
                whale_factor = min(float(10), amplitude / price_change_ratio)

            if whale_factor >= MINIMUM_WHALE_FACTOR:
                write(f"symbol={json_message['data']['s']} \tamplitude={amplitude}\tcandle={candle_color}\t{whale_factor}")
    except Exception as e:
        write(e)
        exit()


def on_open(_):
    write('opened connection')


def on_close(_):
    write('closed connection')


atexit.register(exit_handler)
try:
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()
except Exception as e:
    write(e)
