from time import sleep
from helpers import downloadFile
from helpers import createFolder
from config import coinsDict
from config import typesList
from config import daysCount


def main():
    for coinName in coinsDict:
        coinCode = coinsDict[coinName]
        for typeString in typesList:
            createFolder(f'{coinName}_{typeString}')
            fromTimestamp = 1609459200
            toTimestamp = 1609545600
            for day in range(daysCount):
                # Save the files to appropriate temporary locations
                url = f'https://www.coingecko.com/{typeString}/{coinCode}/usd/custom.json?from={fromTimestamp}&to={toTimestamp}'
                fileName = f'{coinName}_{typeString}/day_{day}.json'
                downloadFile(url, fileName)
                # Increase the range by 1 day == 86400 seconds
                fromTimestamp = toTimestamp
                toTimestamp += 86400
                # Sleep to avoid possible rate-limitations
                sleep(0.01)


if __name__ == "__main__":
    main()
