from pathlib import Path
from requests import get
from datetime import datetime
from pandas import Timestamp


def createFolder(path):
    # Skips if folder already exists
    return Path(path).mkdir(parents=True, exist_ok=True)


def downloadFile(url, fileName):
    # Open the file in binary mode
    with open(fileName, "wb") as file:
        response = get(url)  # Get request
        file.write(response.content)  # Write to the file


def roundTimestamp(inputEpoch):
    return int(Timestamp(inputEpoch, unit='s').round('60min').timestamp())


class DataPoint:
    bitcoin_market_cap = None
    bitcoin_price = None
    bitcoin_volume = None
    dogecoin_market_cap = None
    dogecoin_price = None
    dogecoin_volume = None

    def __str__(self):
        return f'DogecoinPrice:{self.dogecoin_price},DogecoinMarketCap:{self.dogecoin_market_cap},DogecoinVolume:{self.dogecoin_volume},BitcoinPrice:{self.bitcoin_price},BitcoinMarketCap:{self.bitcoin_market_cap},BitcoinVolume:{self.bitcoin_volume}'
