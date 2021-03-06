from datetime import datetime


def create_socket_string():
    coins = []
    with open("watchedcoins.txt", 'r') as f:
        for line in f.readlines():
            coins.append(f"{line.strip()}usdt")

    coins_part = ""
    for coin in coins:
        coins_part += f"{coin}@kline_1m/"

    return f"wss://stream.binance.com:9443/stream?streams={coins_part[:-1]}"


def abort(message, exception):
    write(message)
    write(exception)
    exit()


def write(s, newLine=False):
    if newLine:
        print(f"\n{datetime.now().strftime('%y-%m-%d %H:%M:%S')} - {s}")
    else:
        print(f"{datetime.now().strftime('%y-%m-%d %H:%M:%S')} - {s}")
