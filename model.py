from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Float, create_engine, MetaData
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///test.db')
meta = MetaData(engine)
Base = declarative_base(metadata=meta)
# Base.metadata.create_all()

# meta.create_all()
# class User(BASE):
#     __tablename__ = 'User'

#     id = Column(BigInteger, primary_key=True)
#     username = Column(String(15), unique=True, nullable=False)
#     followers = Column(BigInteger, nullable=False)

class Tweets(Base):
    __tablename__ = 'tweets'

    id = Column(BigInteger, primary_key=True)
    tweet = Column(String(200), unique=True, nullable=False)
    timestamp = Column(String, nullable=False)
    longitude = Column(Float)
    latitude = Column(Float)
    # user_id = Column(BigInteger, ForeignKey('User.id'), nullable=False)
    # user = relationship(User , backref=backref('Tweets'))