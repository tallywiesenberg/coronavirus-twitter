'''Script for filling DB with Twitter Streamer tweets'''

from decouple import config
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

import tweepy

from .model import *
from .stream.streamer import MyStreamListener

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET')) 
TWITTER = tweepy.API(TWITTER_AUTH)   

Base.metadata.create_all()

myStreamListener = MyStreamListener(TWITTER)

streamer = tweepy.Stream(auth=TWITTER_AUTH, listener=myStreamListener)

streamer.filter(track=['#COVID2019', '#COVID', '#Coronavirus'])

streamer.disconnect()