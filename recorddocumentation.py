import os


def recorddocumentation(symbol, time):
    dateYMD = time.strftime('%y-%m-%d')
    filename = f'records/{dateYMD}.txt'

    if not os.path.isfile(filename):
        access = 'w'
    else:
        access = 'a'

    with open(filename, access) as f:
        f.write(f"{time.strftime('%y-%m-%d %H-%M-%S')} - {symbol}\n")
