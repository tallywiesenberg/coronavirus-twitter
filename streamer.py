from model import Tweets, engine

from sqlalchemy.orm import sessionmaker
import tweepy

#Instantiate session
Session = sessionmaker(bind=engine)
session = Session()

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        #Set API
        self.api = api
        #Establish DB Connection
        # self.db = create_engine('sqlite:///test.db')
        # #Instantiate session
        # self.Session = sessionmaker(bind=self.db)
        # self.session = self.Session()
        # #Create tables
        # self.meta = MetaData(self.db)
        # self.meta.create_all()
    def on_status(self, status):
        # connect to DB
#         curs = self.db.cursor()
        # Exclude retweets
        if 'RT @' not in status.text:
            # Choose only geotagged tweets in United States
            if (status.place != None) and (status.place.country_code == 'US'):
            #Try to write tweet information to db
                try:
    #                 user = User(id=status.user.id, username=status.user.screen_name,
    #                             followers=status.user.followers_count)
                    tweet = Tweets(id=status.id, tweet=status.text, timestamp=status.created_at,
                                longitude=sum([pair[0] for pair in status.place.bounding_box.coordinates[0]])/4,
                                latitude=sum([pair[1] for pair in status.place.bounding_box.coordinates[0]])/4,
    #                                user_id=status.user.id
                                )
    #                 self.session.add(user)
                    session.add(tweet)
                    session.commit()
                    print(status.text, status.user.location, status.place.name)
                    #if error occurs
                except Exception as e:
                    print(e)
                    session.rollback()
                    pass