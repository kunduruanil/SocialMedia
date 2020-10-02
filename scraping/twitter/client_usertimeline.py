"""
@author Manish Khati, Anil Kumar Reddy Kunduru
@Date 2nd oct 2020
"""


import sys
import json
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Cursor


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


def get_user_timeline(users):
    for user in users:
        try:
            client = get_twitter_client()
            fname = "user_timeline_{}.jsonl".format(user)
            with open(fname, 'w') as f:
                for page in Cursor(client.user_timeline, screen_name=user,
                                   count=200).pages(16):
                    for status in page:
                        f.write(json.dumps(status._json) + "\n")
        # TBD - write a code to dump json file into DB........
        ## Twitter has limit of 3200 tweets, chk for duplicate before inserting into DB
        except KeyError:
            sys.stderr.write("TWITTER_* environment variables not set\n")


if __name__ == '__main__':
    print(get_user_timeline(["kunduruanil"]))
