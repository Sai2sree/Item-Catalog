from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Book(Base):
    __tablename__ = 'book'

    picture = Column(String(2000)) 
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    author = Column(String(250))
    description = Column(String(20000))
    price = Column(String(8))
    rating = Column(String(250))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'picture' : self.picture,
            'name': self.name,
            'author' : self.author,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'rating': self.rating,
        }


engine = create_engine('sqlite:///genresofbookswithusers.db')


Base.metadata.create_all(engine)
