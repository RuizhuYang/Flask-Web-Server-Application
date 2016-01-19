###configuration###
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#indicate to this is a sepecial sqlalchemy class instance 
#that corrsponds to the tables in database
Base = declarative_base()

###class###
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Cuisine(Base):
    __tablename__ = 'cuisine'

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


class Dish(Base):
    __tablename__ = 'dish'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    cuisine_id = Column(Integer, ForeignKey('cuisine.id'))
    cuisine = relationship(Cuisine)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }

###configuration###
engine = create_engine('sqlite:///cuisinewithusers.db')
#go to te database and add the table created
Base.metadata.create_all(engine)