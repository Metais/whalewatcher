

class DocumentingProcess:
    def __init__(self, time_to_execute, symbol, filename, time_interval):
        self.time_to_execute = time_to_execute
        self.symbol = symbol
        self.filename = filename
        self.time_interval = time_interval

    def document_process(self, closing_price):
        with open(f"coins/{self.symbol}/{self.filename}", 'a') as f:
            # finds the starting price at '0m: *price*' on line 2
            start_price = float(f.readlines()[1].split()[1].strip())
            price_change = (closing_price - start_price) / start_price
            price_change = round(price_change * 100, 2)
            f.write(f"{self.time_interval}m: {closing_price}\t{price_change}%\n")
