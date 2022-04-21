from helpers import DataPoint
from helpers import round_timestamp
from helpers import create_folder
from config import coins_dict
from config import types_list
from config import days_count
import csv
import json


def main():
    # prepare the empty dataset template
    print("Initializing an empty dataset..")
    dataset = {}
    begin_epoch = 1609372800  # December 31, 2020 12:00:00 AM
    end_epoch = 1619913600  # May 2, 2021 12:00:00 AM
    one_hour = 3600  # Seconds
    for i_epoch in range(begin_epoch, end_epoch, one_hour):
        dataset[i_epoch] = DataPoint()

    # iterate over the files and construct the dataset
    print("Combining previously fetched datasets..")
    for coin_name in coins_dict:
        for type in types_list:
            for day in range(days_count):
                # use the previously formatted path to retrieve the file
                file_name = f'raw_datasets/{coin_name}_{type}/day_{day}.json'
                with open(file_name, 'r') as file:
                    file_content = file.read()
                    data_obj = json.loads(file_content)
                    if (type == 'price_charts'):
                        price_data = data_obj['stats']
                        for i in price_data:
                            i_epoch = round_timestamp(i[0]//1000)
                            i_price = i[1]
                            if (coin_name == 'dogecoin'):
                                dataset[i_epoch].dogecoin_price = i_price
                            elif (coin_name == 'bitcoin'):
                                dataset[i_epoch].bitcoin_price = i_price
                        volume_data = data_obj['total_volumes']
                        for i in volume_data:
                            i_epoch = round_timestamp(i[0]//1000)
                            i_volume = i[1]
                            if (coin_name == 'dogecoin'):
                                dataset[i_epoch].dogecoin_volume = i_volume
                            elif (coin_name == 'bitcoin'):
                                dataset[i_epoch].bitcoin_volume = i_volume
                    elif (type == 'market_cap'):
                        market_cap_data = data_obj['stats']
                        for i in market_cap_data:
                            i_epoch = round_timestamp(i[0]//1000)
                            i_market_cap = i[1]
                            if (coin_name == 'dogecoin'):
                                dataset[i_epoch].dogecoin_market_cap = i_market_cap
                            elif (coin_name == 'bitcoin'):
                                dataset[i_epoch].bitcoin_market_cap = i_market_cap

    # format the dataset appropriate for CSV files
    formatted_dataset = []
    for timestamp in dataset:
        data_point = dataset[timestamp]
        formatted_dataset.append({
            'timestamp': timestamp,
            'dogecoin_price': data_point.dogecoin_price,
            'dogecoin_market_cap': data_point.dogecoin_market_cap,
            'dogecoin_volume': data_point.dogecoin_volume,
            'bitcoin_price': data_point.bitcoin_price,
            'bitcoin_market_cap': data_point.bitcoin_market_cap,
            'bitcoin_volume': data_point.bitcoin_volume,
        })

    csv_fields = ['timestamp', 'dogecoin_price', 'dogecoin_market_cap',
                  'dogecoin_volume', 'bitcoin_price', 'bitcoin_market_cap', 'bitcoin_volume']

    create_folder('processed_datasets')
    print("Saving the combined dataset..")
    with open('processed_datasets/price_history.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()
        row_count = 0
        for data in formatted_dataset:
            write_flag = True
            for field_name in csv_fields:
                if data[field_name] == None:
                    write_flag = False

            if write_flag:
                writer.writerow(data)
                row_count += 1

    print(f'Successfully wrote {row_count} rows!')


if __name__ == '__main__':
    main()
