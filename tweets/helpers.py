import re as re
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path


def custom_date_parser(date_string):
    return pd.to_datetime(date_string, format='%Y-%m-%d %H:%M:%S', errors='coerce')


def round_datetime_string(datetime_string):
    dateTime = datetime.fromisoformat(datetime_string)
    return round_datetime(dateTime)


def round_datetime(datetime):
    return int(pd.Timestamp(int(datetime.timestamp()), unit='s').round('60min').timestamp())


def create_folder(path):
    # skip if the folder already exists
    return Path(path).mkdir(parents=True, exist_ok=True)


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt


def clean_tweets(tweets):
    # remove twitter Return handles (RT @xxx:)
    tweets = np.vectorize(remove_pattern)(tweets, "RT @[\w]*:")
    # remove twitter handles (@xxx)'
    tweets = np.vectorize(remove_pattern)(
        tweets, "@[\w]*")
    # remove URL links (httpxxx)
    tweets = np.vectorize(remove_pattern)(
        tweets, "https?://[A-Za-z0-9./]*")
    # remove special characters, numbers, punctuations (except for #)
    tweets = np.core.defchararray.replace(tweets, "[^a-zA-Z]", " ")

    return tweets


def dateparse(time_in_secs):
    return datetime.fromtimestamp(float(time_in_secs))
