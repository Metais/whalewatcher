import websocket
import json
import config
import time
import atexit
import os
import documentingwhales

from binance.client import Client
from utils import write, create_socket_string, abort
from datetime import datetime, timedelta

# TODO Add an administrative file that logs when a new file is created
# TODO Add a restriction on documenting whales if they're too close to each other

WHALE_CUTOFF = 0.017  # % change in a minute candle that would describe a whale purchase/sell
MINIMUM_WHALE_FACTOR = 3.5  # minimum accepted ratio between upper wick and price change to be considered whale purchase

# after how many minutes to write price interval, ranges from 5 minutes after whale event to 1 day after whale event
time_intervals = [1, 5, 10, 30, 60, 120, 240, 720, 1440]

socket = create_socket_string()
client = Client(config.API_KEY, config.API_SECRET)
documenting_processes = []


def exit_handler():
    write("Closing program...")


def document_whale(symbol, closing_price, amplitude, whale_factor):
    global documenting_processes  # necessary?

    # check is directory for the symbol already exists or not
    if not os.path.isdir(f'coins/{symbol}'):
        write(f"Making a directory for symbol {symbol}")
        os.mkdir(f'coins/{symbol}')

    current_time = datetime.now()

    with open(f"coins/{symbol}/{current_time.strftime('%y-%m-%d %H-%M-%S')}.txt", 'w') as f:
        amplitude = round(amplitude * 100, 2)
        whale_factor = round(whale_factor, 2)
        write(f"Writing first 2 lines for file {f.name}")
        f.write(f"{symbol}\tamplitude= +{amplitude}%\twhalefactor={whale_factor}\n")
        f.write(f"0m: {closing_price}\n")

        processes = []
        for time_interval in time_intervals:
            execute_time = current_time + timedelta(minutes=time_interval)
            process = documentingwhales.DocumentingProcess(execute_time, symbol, f.name, time_interval)
            processes.append(process)

    documenting_processes.extend(processes)
    write(f"Adding processes to the list of processes, now holding {len(documenting_processes)} processes...")


def on_message(_, message):
    try:
        json_message = json.loads(message)

        # ignore if unclosed candle
        is_candle_closed = json_message['data']['k']['x']
        if not is_candle_closed:
            return

        symbol = json_message['data']['s']
        opening_price = float(json_message['data']['k']['o'])
        closing_price = float(json_message['data']['k']['c'])
        high_price = float(json_message['data']['k']['h'])

        # check if there are processes that need to be executed
        processes_for_symbol = [x for x in documenting_processes if x.symbol == symbol and x.time_to_execute <=
                                datetime.now() + timedelta(seconds=10)]
        for process in processes_for_symbol:
            write(f"Documenting change for symbol={symbol}, filename={process.filename}, "
                  f"time interval={process.time_interval}", newLine=True)
            process.document_process(closing_price)
            documenting_processes.remove(process)

        # with this program, we're not interested in the 'lowest' price of a candle
        # amplitude is best measured as the ratio of highest price to opening price
        # basically, we don't care about 'bottom-wicks', since it could flag high amplitude for wrong reasons
        amplitude = (high_price - opening_price) / opening_price

        if amplitude > WHALE_CUTOFF:
            # for determining candle color
            price_change = closing_price - opening_price
            candle_color = "red" if price_change < 0 else "green" if price_change > 0 else "unchanged"

            # for determining chance that this was a whale (high number == high chance of whale)
            price_change_ratio = price_change / opening_price
            if price_change_ratio < 0.001:
                whale_factor = 10
            else:
                whale_factor = min(float(10), amplitude / price_change_ratio)

            if whale_factor >= MINIMUM_WHALE_FACTOR:
                write(f"symbol={symbol} \tamplitude={amplitude}\tcandle={candle_color}\t{whale_factor}", newLine=True)
                document_whale(symbol, closing_price, amplitude, whale_factor)
            else:
                write(f"symbol={symbol} \tamplitude={amplitude}\tcandle={candle_color}\t{whale_factor}\n"
                      f"The whale factor was too low...", newLine=True)
    except Exception as e:
        abort("something went wrong in the main message function", e)


def on_open(_):
    write('opened connection')


def on_close(_):
    write('closed connection')


atexit.register(exit_handler)
try:
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()
except Exception as e:
    abort("Something went wrong with the websocket", e)
