# Cleans all news headlines and fetches the players featured today
# File: NewsCleaner.py
# Names: Jaison Jose, Neha Joshi, Pranav Karnani, Preet Jain
import os
import nltk
import pandas as pd

from nltk.corpus import stopwords

FILE_PATH = os.path.abspath(os.path.join(__file__, '..'))
ROOT_DIR = os.path.abspath(os.path.join(FILE_PATH, '..'))
DATA_PATH = ROOT_DIR + '/data/'

# Downloads stop words
# Called when data is scraped, from PlayerSpider
nltk.download('stopwords')
stop_words = stopwords.words('english')

def clean_news():
    fpl = pd.read_csv(DATA_PATH+'season_player_stats_df.csv')
    news_df = pd.read_csv(DATA_PATH+'news.csv')

    # Removes all stopwords
    news_df['news_clean'] = news_df['news'].apply(lambda x: ' '.join([word for word in x.split()
                                                                      if word not in stop_words]))
    web_names = list(fpl['web_name'])
    news_processed = list(news_df['news_clean'])

    # Checks for players mentioned in the news
    featured = {}
    for headline in news_processed:
        for name in web_names:
            if name in headline:
                if name in featured.keys():
                    featured[name] += 1
                else:
                    featured[name] = 1

    # Creates a dataframe with the last of players featured today
    featured_df = pd.DataFrame(featured.items(), columns=['Player', 'Times'])
    featured_df.to_csv(DATA_PATH+'featured.csv')