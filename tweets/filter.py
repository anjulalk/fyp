import pandas as pd
from helpers import round_datetime
from helpers import custom_date_parser
from helpers import create_folder
from helpers import clean_tweets
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
csv_url = './raw_datasets/doge_tweets_1.1.21-4.30.21.csv'
csv_datatypes = {
    'created_at': 'string',
    'tweet': 'string',
    'username': 'string',
    'language': 'string',
    'replies_count': 'UInt32',
    'retweets_count': 'UInt32',
    'likes_count': 'UInt32',
    'retweet': 'boolean',
    'hashtags': 'object',
}


def main():
    print("Processing the dataset..")
    # data = pd.read_csv(csv_url, usecols=csv_datatypes.keys(), nrows=1000,
    #                    dtype=csv_datatypes, error_bad_lines=False, parse_dates=[0], date_parser=custom_date_parser)
    data = pd.read_csv(csv_url, usecols=csv_datatypes.keys(),
                       dtype=csv_datatypes, error_bad_lines=False, parse_dates=[0], date_parser=custom_date_parser)

    print("Deleting rows with missing values...")
    data.dropna(inplace=True)

    print("Size:", data.size)

    print("Deleting retweets...")
    data = data[data['retweet'] == False]

    print("Size:", data.size)

    print("Deleting non-English tweets...")
    data = data[data['language'] == 'en']

    print("Size:", data.size)

    print("Mapping created_at values to timestamp values...")
    data['timestamp'] = data['created_at'].map(round_datetime)

    print("Deleting created_at column...")
    data.drop(columns=['created_at'], inplace=True)

    print("Reordering the dataframe...")
    data = data[['timestamp'] + list(csv_datatypes.keys())[1:]]

    print("Identifying users with two or more identical tweets...")
    username_tweets = data.groupby('username').agg(tweet_list=(
        'tweet', lambda x: list(x)), tweet_set=('tweet', lambda x: set(map(crop, x))))
    username_tweets_flagged = username_tweets[username_tweets['tweet_list'].map(
        len) != username_tweets['tweet_set'].map(len)]

    print("Deleting tweets with flagged usernames...")
    data = data[data['username'].isin(username_tweets_flagged.index) == False]

    print("Size:", data.size)

    print("Cleaning the tweets for sentiment analysis...")
    data['tweet_clean'] = clean_tweets(data['tweet'])

    print("Deleting rows with missing values...")
    data.dropna(inplace=True)

    print("Analyzing sentiment scores of the tweets...")
    data['compound_score'] = data['tweet_clean'].map(
        lambda x: analyzer.polarity_scores(x)["compound"], na_action='ignore')
    data['positive_score'] = data['tweet_clean'].map(
        lambda x: analyzer.polarity_scores(x)["pos"], na_action='ignore')
    data['neutral_score'] = data['tweet_clean'].map(
        lambda x: analyzer.polarity_scores(x)["neu"], na_action='ignore')
    data['negative_score'] = data['tweet_clean'].map(
        lambda x: analyzer.polarity_scores(x)["neg"], na_action='ignore')

    print("Neutral Tweets:", data.query("neutral_score == 1").shape[0])
    print("Total Tweets:", data.shape[0])

    create_folder('./processed_datasets')

    print("Saving the processed dataset...")
    data.to_csv('processed_datasets/tweets_filtered.csv', index=False)

    print(f'Successfully wrote {data.shape[0]} rows!')

    print("Saving the identified spam tweets...")
    username_tweets_flagged.to_csv(
        'processed_datasets/tweets_spam.csv', index=False)


def crop(tweet):
    if len(tweet) < 5:
        return tweet
    else:
        return tweet[:5]


def converter(x):
    if isinstance(x, pd.Series):
        return tuple(x.values)
    else:
        return x


main()
