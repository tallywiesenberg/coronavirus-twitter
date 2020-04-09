'''DB Framework with SQLAlchemy'''

from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Float, create_engine, MetaData
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///tweets.db')
meta = MetaData(engine)
Base = declarative_base(metadata=meta)

class Tweets(Base):
    __tablename__ = 'tweets'

    id = Column(BigInteger, primary_key=True)
    tweet = Column(String(200), unique=True, nullable=False)
    timestamp = Column(String, nullable=False)
    longitude = Column(Float)
    latitude = Column(Float)