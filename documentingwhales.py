from datetime import datetime


class DocumentingProcess:
    def __init__(self, time_to_execute, symbol, filename, time_interval):
        self.time_to_execute = time_to_execute
        self.symbol = symbol
        self.filename = filename
        self.time_interval = time_interval

    def document_process(self, closing_price):
        with open(f"{self.filename}", 'r') as f:
            # finds the starting price at '0m: *price*' on line 2
            start_price = float(f.readlines()[1].split()[1].strip())

        with open(f"{self.filename}", 'a') as f:
            price_change = (closing_price - start_price) / start_price
            price_change = round(price_change * 100, 2)
            f.write(f"{datetime.now().strftime('%y-%m-%d %H-%M-%S')} {self.time_interval}m: {closing_price}\t{price_change}%\n")
