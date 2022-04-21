from pathlib import Path
from requests import get
from pandas import Timestamp


def create_folder(path):
    # skip if the folder already exists
    return Path(path).mkdir(parents=True, exist_ok=True)


def download_file(url, file_name):
    # open the file in binary mode
    with open(file_name, "wb") as file:
        response = get(url)  # GET request
        file.write(response.content)  # write to the file


def round_timestamp(in_epoch):
    return int(Timestamp(in_epoch, unit='s').round('60min').timestamp())


class DataPoint:
    bitcoin_market_cap = None
    bitcoin_price = None
    bitcoin_volume = None
    dogecoin_market_cap = None
    dogecoin_price = None
    dogecoin_volume = None

    def __str__(self):
        return f'DogecoinPrice:{self.dogecoin_price},DogecoinMarketCap:{self.dogecoin_market_cap},DogecoinVolume:{self.dogecoin_volume},BitcoinPrice:{self.bitcoin_price},BitcoinMarketCap:{self.bitcoin_market_cap},BitcoinVolume:{self.bitcoin_volume}'
