import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


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
    # data = pd.read_csv(csv_url, usecols=csv_datatypes.keys(),
    #                    cache_dates=True, nrows=1000)
    data = pd.read_csv(csv_url, usecols=csv_datatypes.keys(), cache_dates=True)

    stopwords = set(STOPWORDS)
    with open("stopwords.txt") as file:
        word_list = file.readlines()
        for word in word_list:
            stopwords.add(word.strip())

    tweets = data['tweet'].values
    word_cloud = WordCloud(stopwords=stopwords,
                           background_color="white",
                           max_words=2000,
                           min_word_length=4,
                           min_font_size=12,
                           width=800,
                           height=600).generate(' '.join(tweets))

    plt.imshow(word_cloud)
    plt.axis("off")
    plt.savefig('word_cloud.png')

    print(f'Successfully derrived word cloud for {data.shape[0]} rows!')


main()
