import pandas as pd

csv_url = './processed_datasets/tweets_filtered.csv'
csv_datatypes = {
    'timestamp': 'UInt32',
    'tweet': 'string',
    'username': 'string',
    'replies_count': 'UInt32',
    'retweets_count': 'UInt32',
    'likes_count': 'UInt32',
    'compound_score': 'float16',
    'positive_score': 'float16',
    'negative_score': 'float16',
    'neutral_score': 'float16',
}


def main():
    print("Reading the dataset..")
    # data = pd.read_csv(csv_url, usecols=csv_datatypes.keys(), cache_dates=True, nrows=1000)
    data = pd.read_csv(csv_url, usecols=csv_datatypes.keys(), cache_dates=True)

    print("Aggregating the dataset...")
    data = data.groupby('timestamp').agg(
        tweets_count=('tweet', 'nunique'),
        usernames_count=('tweet', 'nunique'),
        likes_sum=('likes_count', 'sum'),
        replies_sum=('replies_count', 'sum'),
        retweets_sum=('retweets_count', 'sum'),
        compound_score_sum=('compound_score', 'sum'),
        positive_score_sum=('positive_score', 'sum'),
        negative_score_sum=('negative_score', 'sum'),
        neutral_score_sum=('neutral_score', 'sum'),
        likes_mean=('likes_count', 'mean'),
        replies_mean=('replies_count', 'mean'),
        retweets_mean=('retweets_count', 'mean'),
        compound_score_mean=('compound_score', 'mean'),
        positive_score_mean=('positive_score', 'mean'),
        negative_score_mean=('negative_score', 'mean'),
        neutral_score_mean=('neutral_score', 'mean'),
    ).reset_index()

    print("Saving the processed dataset...")
    data.to_csv('processed_datasets/tweets_count.csv', index=False)

    print(f'Successfully wrote {data.shape[0]} rows!')


main()
