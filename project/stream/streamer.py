'''Custom Twitter streamer using Tweepy/Twitter API'''

from project.model import Tweets, engine

from sqlalchemy.orm import sessionmaker
import tweepy

#Instantiate session
Session = sessionmaker(bind=engine)
session = Session()

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        #Set API
        self.api = api
    def on_status(self, status):
        # Exclude retweets
        if 'RT @' not in status.text:
            # Choose only geotagged tweets in United States
            if (status.place != None) and (status.place.country_code == 'US'):
            #Try to write tweet information to db
                try:
                    try:
                        tweet = Tweets(id=status.id, tweet=status.extended_tweet['full_text'], timestamp=status.created_at,
                                    longitude=sum([pair[0] for pair in status.place.bounding_box.coordinates[0]])/4,
                                    latitude=sum([pair[1] for pair in status.place.bounding_box.coordinates[0]])/4)
                        session.add(tweet)
                        session.commit()
                        print(status.extended_tweet['full_text'], status.user.location, status.place.name)
                    except AttributeError as e:
                        tweet = Tweets(id=status.id, tweet=status.text, timestamp=status.created_at,
                                    longitude=sum([pair[0] for pair in status.place.bounding_box.coordinates[0]])/4,
                                    latitude=sum([pair[1] for pair in status.place.bounding_box.coordinates[0]])/4)
                        session.add(tweet)
                        session.commit()
                        print(status.text, status.user.location, status.place.name)
                    #if error occurs
                except Exception as e:
                    print(e)
                    session.rollback()
                    pass