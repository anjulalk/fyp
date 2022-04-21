import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from datetime import datetime
from pathlib import Path
from numpy import isnan


def custom_date_parser(date_string):
    return pd.to_datetime(date_string, format='%Y-%m-%d %H:%M:%S', errors='coerce')


def round_datetime_string(datetime_string):
    dateTime = datetime.fromisoformat(datetime_string)
    return round_datetime(dateTime)


def round_datetime(datetime):
    return int(pd.Timestamp(int(datetime.timestamp()), unit='s').round('60min').timestamp())


def create_folder(path):
    # skips if the folder already exists
    return Path(path).mkdir(parents=True, exist_ok=True)


def dateparse(time_in_secs):
    return datetime.fromtimestamp(float(time_in_secs))


def plot_confusion_matrix(data, labels):
    sns.set(color_codes=True)
    plt.figure(1, figsize=(9, 6))

    plt.title("Confusion Matrix")

    sns.set(font_scale=1.4)
    ax = sns.heatmap(data, annot=True, fmt='g', cmap="YlGnBu",
                     cbar_kws={'label': 'Scale'})

    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    ax.set(ylabel="True Label", xlabel="Predicted Label")

    plt.show()


def fill_missing(values):
    one_hour = 60
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            if isnan(values[row, col]):
                values[row, col] = values[row - one_hour, col]
