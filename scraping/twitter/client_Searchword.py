"""
@author Manish Khati, Anil Kumar Reddy Kunduru
@Date 2nd oct 2020
"""


import sys
import json
import datetime
from datetime import date
import pandas as pd
import numpy as np
import preprocessor as p

from tweepy import API
from tweepy import OAuthHandler
from twitter_nlp_toolkit.twitter_listener import twitter_listener
from tweepy import Cursor
from scraping.twitter.client_usertimeline import get_twitter_client
from app_route.all_apis import insert_search_keyword_sentiment

from afinn import Afinn
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app_route.all_apis import add_dataframe
import configration.constants as config

def get_twitter_auth():
    print('get_twitter_auth')
    """Setup Twitter authentication.
    Return: tweepy.OAuthHandler object
    """
    with open('keys.key', 'r') as infile:
        # print(infile)
        credentials = json.load(infile)
    try:
        consumer_key = credentials['consumer_key']  # api_key
        consumer_secret = credentials['consumer_secret']  # api_secret_key
        access_token = credentials['access_token']  # access_token
        access_secret = credentials['access_secret']  # access_token_secret
        # print(credentials)
    except KeyError:
        sys.stderr.write("TWITTER_* environment variables not set\n")
        sys.exit(1)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth


def get_twitter_client():
    print('Enter get_twitter_client')
    """Setup Twitter API client.
    Return: tweepy.API object
    """
    auth = get_twitter_auth()
    client = API(auth)
    return client


def get_tweets_search_list(searchlist):
    today = date.today()
    yesterday = today - datetime.timedelta(days=1)
    for keyword in searchlist:
        try:
            client = get_twitter_client()
            tweets = Cursor(client.search, q=keyword, lang='en', since=yesterday, until=today, ).items(20)
            tweets_list = [[tweet.id, tweet.created_at, tweet.source, tweet.text, tweet.retweeted, tweet.retweet_count,
                            tweet.favorite_count] for tweet in tweets]
            # Creation of dataframe from tweets list
            # Add or remove columns as you remove tweet information
            tweets_df = pd.DataFrame(tweets_list)
            col = ['ID', 'Created_At', 'Source', 'Original_Text', 'Is_Retweeted', 'Retweet_count',
                                 'Like_count']
            tweets_df.columns = col
            tweets_df['Clean_Text'] = tweets_df['Original_Text'].apply(p.clean)
            tweets_df["Created_At"] = pd.to_datetime(tweets_df["Created_At"])
            return tweets_df

        # TBD - write a code to dump json file into DB........
        ## Twitter has limit of 3200 tweets, chk for duplicate before inserting into DB
        except KeyError:
            sys.stderr.write("TWITTER_* environment variables not set\n")


# Function used to analyze the text in hte dataframe
def analyze_text(input_text, analyzer):
    af = Afinn()
    analyser = SentimentIntensityAnalyzer()
    if analyzer == 'VADER':
        result = analyser.polarity_scores(input_text)
    elif analyzer == 'TextBlob':
        result = TextBlob(input_text).sentiment.polarity
    elif analyzer == 'Afinn':
        result = af.score(input_text)
    return result


def Final_Sentiment(row):
    if (row['VADER_Sentiment'] == 'Positive' and row['Textblob_Sentiment'] == 'Positive' and row[
        'Afinn_Sentiment'] == 'Positive'):
        final_sentiment = 'Positive'
    elif (row['VADER_Sentiment'] == 'Positive' and row['Textblob_Sentiment'] == 'Positive'):
        final_sentiment = 'Positive'
    elif (row['VADER_Sentiment'] == 'Positive' and row['Afinn_Sentiment'] == 'Positive'):
        final_sentiment = 'Positive'
    elif (row['Textblob_Sentiment'] == 'Positive' and row['Afinn_Sentiment'] == 'Positive'):
        final_sentiment = 'Positive'
    elif (row['VADER_Sentiment'] == 'Negative' and row['Textblob_Sentiment'] == 'Negative' and row[
        'Afinn_Sentiment'] == 'Negative'):
        final_sentiment = 'Negative'
    elif (row['VADER_Sentiment'] == 'Negative' and row['Textblob_Sentiment'] == 'Negative'):
        final_sentiment = 'Negative'
    elif (row['VADER_Sentiment'] == 'Negative' and row['Afinn_Sentiment'] == 'Negative'):
        final_sentiment = 'Negative'
    elif (row['Textblob_Sentiment'] == 'Negative' and row['Afinn_Sentiment'] == 'Negative'):
        final_sentiment = 'Negative'
    else:
        final_sentiment = 'Neutral'
    return final_sentiment


def sentiment_analysis(df):
    analyzer_lst = ['VADER', 'TextBlob', 'Afinn']
    for i in analyzer_lst:
        if i == 'VADER':
            Neg = i + "_Neg"
            Neu = i + "_Neu"
            Pos = i + "_Pos"
            Comp = i + "_Comp"
        else:
            col_Name = i + "_score"
        for j in range(df.shape[0]):
            temp = analyze_text(df.loc[j, 'Clean_Text'], analyzer=i)
            if i == 'VADER':
                df.loc[j, Neg] = temp['neg']
                df.loc[j, Neu] = temp['neu']
                df.loc[j, Pos] = temp['pos']
                df.loc[j, Comp] = temp['compound']
            else:
                df.loc[j, col_Name] = temp
    df['VADER_Sentiment'] = df['VADER_Comp'].apply(
        lambda x: 'Positive' if x > .05 else ('Neutral' if x < .05 and x > -0.05 else 'Negative'))
    df['Textblob_Sentiment'] = df['TextBlob_score'].apply(
        lambda x: 'Positive' if x > .05 else ('Neutral' if x < .05 and x > -0.05 else 'Negative'))
    df['Afinn_Sentiment'] = df['Afinn_score'].apply(
        lambda x: 'Positive' if x > .05 else ('Neutral' if x < .05 and x > -0.05 else 'Negative'))

    df['Sentiment'] = df.apply(Final_Sentiment, axis=1)
    ## mongo db added data
    #obj = add_dataframe(df=df, collection_name=config.serach_keywords)
    #data = df["Sentiment"].value_counts().to_dict()
    return df

def get_hourly_stats(df):
    """

    :param df:
    :return:
    """
    df = df[["Created_At", "Sentiment"]]
    df.loc[:,"Created_At"] = pd.to_datetime(df.loc[:,"Created_At"])
    df.loc[:,"Created_At"] = df.loc[:,"Created_At"].dt.round("H")
    hourly = pd.DataFrame({"count": df.groupby(["Created_At", "Sentiment"]).size()}).reset_index(level=[1])
    hourly_count = dict()
    for i in hourly.index.unique():
        hourly_count[i.isoformat()] = dict(zip(hourly.loc[i, "Sentiment"].tolist(), hourly.loc[i, "count"].tolist()))
    return hourly_count

def tweets_search_insert(searchlist,user_id):
    """

    :param searchlist:
    :return:
    """
    tweet_df = get_tweets_search_list(searchlist)
    df = sentiment_analysis(tweet_df)
    data = dict()
    data["user_id"] = user_id
    data["hourly_stats"] = get_hourly_stats(df)
    data["totalcount"] = tweet_df.shape[0]
    data["source"] = "twitter"
    data["searchlist"] = searchlist
    obj = insert_search_keyword_sentiment(data=data, collection=config.serach_keywords)
    return str(obj)

if __name__ == '__main__':
    searchlist = ["AI"]
    print(tweets_search_insert(searchlist,"5f81659619b72d9082c6ea4e"))
    # tweet_df = get_tweets_search_list(searchlist)
    # df = sentiment_analysis(tweet_df)
    # df.to_csv("datascience.csv")
