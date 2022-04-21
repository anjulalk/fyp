from time import sleep
from helpers import download_file
from helpers import create_folder
from config import coins_dict
from config import types_list
from config import days_count


def main():
    for coin_name in coins_dict:
        coin_code = coins_dict[coin_name]
        for type in types_list:
            create_folder(f'raw_datasets/{coin_name}_{type}')
            from_epoch = 1609459200
            to_epoch = 1609545600
            for day in range(days_count):
                # save the files to appropriate temporary locations
                url = f'https://www.coingecko.com/{type}/{coin_code}/usd/custom.json?from={from_epoch}&to={to_epoch}'
                fileName = f'raw_datasets/{coin_name}_{type}/day_{day}.json'
                download_file(url, fileName)
                # increase the range by 1 day == 86400 seconds
                from_epoch = to_epoch
                to_epoch += 86400
                # sleep to avoid possible rate-limitations
                sleep(0.01)


if __name__ == '__main__':
    main()
