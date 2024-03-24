from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    matric_no = Column(String)
    email = Column(String)
    password = Column(String)
    wallet = Column(Integer)
    rides = relationship("Ride", back_populates="user")
    messages = relationship("Message", back_populates="user")

class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    platenumber = Column(String)
    rides = relationship("Ride", back_populates="driver")
    messages = relationship("Message", back_populates="driver")

class Ride(Base):
    __tablename__ = "ride"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    from_location = Column(String)
    to_location = Column(String)
    price = Column(Integer)
    date = Column(String)
    clas = Column(String)
    seat = Column(Integer)
    bag = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    driver_id = Column(Integer, ForeignKey('driver.id'), nullable=True)
    mobility_constrained = Column(Boolean, default=False)
    cancelled = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
    user = relationship("User", back_populates="rides")
    driver = relationship("Driver", back_populates="rides")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    driver_id = Column(Integer, ForeignKey('driver.id'), nullable=True) 
    user = relationship("User", back_populates="messages")
    driver = relationship("Driver", back_populates="messages")
    message = Column(String)
