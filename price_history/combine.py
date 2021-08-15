from json import loads
from time import time
from helpers import DataPoint
from helpers import roundTimestamp
from config import coinsDict
from config import typesList
from config import daysCount
import csv


def main():
    # Prepare the empty dataset template
    dataset = {}
    beginTimestamp = 1609372800  # December 31, 2020 12:00:00 AM
    endTimestamp = 1619913600  # May 2, 2021 12:00:00 AM
    oneHour = 3600  # Seconds
    for iTimestamp in range(beginTimestamp, endTimestamp, oneHour):
        dataset[iTimestamp] = DataPoint()

    # Iterate over the files and construct the dataset
    for coinName in coinsDict:
        for typeString in typesList:
            for day in range(daysCount):
                # Use the previously formatted path to retrieve the file
                fileName = f'{coinName}_{typeString}/day_{day}.json'
                with open(fileName, 'r') as file:
                    fileContent = file.read()
                    dataObject = loads(fileContent)
                    if (typeString == 'price_charts'):
                        priceData = dataObject['stats']
                        for i in priceData:
                            iTimestamp = roundTimestamp(i[0]//1000)
                            iPrice = i[1]
                            if (coinName == 'dogecoin'):
                                dataset[iTimestamp].dogecoin_price = iPrice
                            elif (coinName == 'bitcoin'):
                                dataset[iTimestamp].bitcoin_price = iPrice
                        volumeData = dataObject['total_volumes']
                        for i in volumeData:
                            iTimestamp = roundTimestamp(i[0]//1000)
                            iVolume = i[1]
                            if (coinName == 'dogecoin'):
                                dataset[iTimestamp].dogecoin_volume = iVolume
                            elif (coinName == 'bitcoin'):
                                dataset[iTimestamp].bitcoin_volume = iVolume
                    elif (typeString == 'market_cap'):
                        marketCapData = dataObject['stats']
                        for i in marketCapData:
                            iTimestamp = roundTimestamp(i[0]//1000)
                            iMarketCap = i[1]
                            if (coinName == 'dogecoin'):
                                dataset[iTimestamp].dogecoin_market_cap = iPrice
                            elif (coinName == 'bitcoin'):
                                dataset[iTimestamp].bitcoin_market_cap = iPrice

    # Format the dataset appropriate for CSV files
    formattedDataset = []
    for timestamp in dataset:
        dataPoint = dataset[timestamp]
        formattedDataset.append({
            'timestamp': timestamp,
            'dogecoin_price': dataPoint.dogecoin_price,
            'dogecoin_market_cap': dataPoint.dogecoin_market_cap,
            'dogecoin_volume': dataPoint.dogecoin_volume,
            'bitcoin_price': dataPoint.bitcoin_price,
            'bitcoin_market_cap': dataPoint.bitcoin_market_cap,
            'bitcoin_volume': dataPoint.bitcoin_volume,
        })

    csvFields = ['timestamp', 'dogecoin_price', 'dogecoin_market_cap',
                 'dogecoin_volume', 'bitcoin_price', 'bitcoin_market_cap', 'bitcoin_volume']
    
    with open("price_history_dataset.csv", 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvFields)
        writer.writeheader()
        rowCount = 0
        for data in formattedDataset:
            writeFlag = True
            for fieldName in csvFields:
                if data[fieldName] == None:
                    writeFlag = False

            if (writeFlag):
                writer.writerow(data)
                rowCount += 1

    print(f'Successfully wrote {rowCount} rows..')


if __name__ == "__main__":
    main()
