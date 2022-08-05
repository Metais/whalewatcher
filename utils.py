from datetime import datetime


def create_socket_string(client):
    """coins = []
    with open("watchedcoins.txt", 'r') as f:
        for line in f.readlines():
            coins.append(f"{line.strip()}usdt")"""

    exchange_info = [x for x in client.get_exchange_info()['symbols'] if x['status'] == 'TRADING']
    coins = [x['symbol'].lower() for x in exchange_info if x['symbol'][-3:] == 'ETH'
             and f"{x['symbol'][:-3]}USDT" in [y['symbol'] for y in exchange_info]]

    excluded_coins = ["galaeth", "slpeth", "farmeth", "mfteth", "straxeth", "qtumeth", "firoeth", "bnteth", "kavaeth",
                      "ezeth", "sceth", "lsketh", "zrxeth", "cvceth", "aioneth", "stmxeth", "xemeth", "cvpeth",
                      "voxeleth", "chreth", "dataeth", "egldeth", "adxeth", "xnoeth", "qlceth", "qkceth", "ufteth",
                      "ghsteth", "icxeth", "iosteth", "funeth", "elfeth", "ncasheth", "mtleth", "dydxeth", "xvgeth",
                      "denteth", "keyeth", "ookieth", "pundixeth", "betaeth", "jasmyeth", "vgxeth"]

    coins = [x for x in coins if x not in excluded_coins]

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
