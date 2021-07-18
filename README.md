A script that keeps track of coins that experience massive orders (purchases from crypto-whales, institutions, hedge-funds), and subsequently tracks what it does to the price in selected price-intervals. Its primary use is the tracking of prices of coins that are subject of large fluctuations.

Symbols that are tracked are USDT markets of coins listed in watchedcoins.txt

Feel free to alter parameters such as WHALE_CUTOFF (%amplitude of a 1m candle), MINIMUM_WHALE_FACTOR (ratio of upper wick to price change) and the price intervals.

Installation manual:
- Use Python 3.6
- Use Miniconda
- Create a virtual environment, as follows: conda create --name yourEnvName python=3.6 
- Activate the virtual environment, as follows: conda activate yourEnvName
- Download the following packages in the following order:
- - conda install -c conda-forge websocket-client
- - conda install pip
- - conda install twisted
- - pip install python-binance
- Run with command 'python main.py' while in root project folder
