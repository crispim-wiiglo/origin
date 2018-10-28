from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Rest(Base):
	__tablename__ = 'restaurant'

	id = Column(Integer, primary_key = True)
	restaurant_name = Column(String)
	restaurant_address = Column(String)
	restaurant_image = Column(String)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
      		'restaurant_name': self.restaurant_name,
      		'restaurant_address': self.restaurant_address,
      		'restaurant_image' : self.restaurant_image,
      		'id' : self.id
      	}
		
engine = create_engine('sqlite:///restaurant.db')
Base.metadata.create_all(engine)
