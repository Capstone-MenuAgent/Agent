from sqlalchemy import Column, Integer, VARCHAR, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

from database.sqlSetting import Engine

Base = declarative_base()

class RestaurantTable(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=False)
    tag = Column(VARCHAR(255), nullable=True)
    rating = Column(Float, nullable=True)
    reviewNum = Column(Integer, nullable=True)
    address = Column(VARCHAR(255))
    url = Column(VARCHAR(1023))
    loc = Column(VARCHAR(255))

    menu = relationship("MenuTable", back_populates="restaurant", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('title', 'address', name='uix_title_address'),)

class MenuTable(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    restaurantId = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship("RestaurantTable", back_populates="menu")

    __table_args__ = (UniqueConstraint('name', 'restaurantId', name='uix_name_restaurantId'),)