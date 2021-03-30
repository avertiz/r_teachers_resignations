import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

def isNaN(string):
        return string != string

def analyze(teachers_file):

    # Import
    print('loading file...')
    data = pd.read_csv(teachers_file)
    print('file loaded')

    # Formatting
    print('formatting...')
    data['resignation_flair'] = data['link_flair_text'] == 'Resignation'
    data['title_contains_resign'] = data['title'].str.contains('resign|Resign|quit')
    data['text_contains_resign'] = (data['selftext'].str.contains('resign|Resign|quit')
                                        .fillna(False)
                                    )
    data['resignation_post'] = (data['link_flair_text'] == 'Resignation') | (data['title_contains_resign'] == True) | (data['text_contains_resign'] == True)
    data['post_date'] = (data['created_utc'].apply(datetime.datetime.fromtimestamp)
                            .dt.tz_localize('utc').dt.tz_convert('US/Central')
                            .apply(datetime.datetime.date)
                        )
    data['post_date'] = pd.to_datetime(data['post_date'])
    data['post_month'] = pd.to_datetime(data['post_date']).dt.to_period('m')
    data['post_year'] = pd.to_datetime(data['post_date']).dt.to_period('Y')
    print('formatting complete')

    # Sentiment Analysis
    print('sentiment analysis...')
    sia = SentimentIntensityAnalyzer()
    neg = []
    neu = []
    pos = []
    for index, row in data.iterrows():
        title_and_text = row['title']
        if not isNaN(row['selftext']):
            title_and_text += ' ' + row['selftext']
        sentiment = sia.polarity_scores(title_and_text)
        neg.append(sentiment['neg'])
        neu.append(sentiment['neu'])
        pos.append(sentiment['pos'])
    data['negative_sentiment'] = neg
    data['neutral_sentiment'] = neu
    data['positive_sentiment'] = pos
    print('sentiment analysis complete')

    return(data)

if __name__ == '__main__':
    data = analyze(teachers_file = 'teachers_cleaned.csv')
    print("Writing to csv")
    data.to_csv('teachers_analysis.csv', index=False)
    print('complete')
