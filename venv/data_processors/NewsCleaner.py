import os
import nltk
import pandas as pd

from nltk.corpus import stopwords

FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
ROOT_DIR = os.path.abspath(os.path.join(FILE_PATH, '..'))
DATA_PATH = ROOT_DIR + '/data/'

nltk.download('stopwords')
stop_words = stopwords.words('english')


def clean_news():
    fpl = pd.read_csv(DATA_PATH+'season_player_stats_df.csv')
    news_df = pd.read_csv(DATA_PATH+'news.csv')

    news_df['news_clean'] = news_df['news'].apply(lambda x: ' '.join([word for word in x.split()
                                                                      if word not in stop_words]))
    web_names = list(fpl['web_name'])
    news_processed = list(news_df['news_clean'])

    featured = {}
    for headline in news_processed:
        for name in web_names:
            if name in headline:
                if name in featured.keys():
                    featured[name] += 1
                else:
                    featured[name] = 1

    return featured

    # news_df.to_csv(DATA_PATH+'news.csv')

clean_news()