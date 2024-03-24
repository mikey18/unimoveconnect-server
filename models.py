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
    messages = relationship("Message", back_populates="user")  # Add this line

class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    platenumber = Column(String)
    rides = relationship("Ride", back_populates="driver")
    messages = relationship("Message", back_populates="driver")  # Add this line

class Ride(Base):
    __tablename__ = "ride"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())  # DateTime field for indicating ride creation time
    from_location = Column(String)
    to_location = Column(String)
    price = Column(Integer)
    date = Column(String)
    clas = Column(String)
    seat = Column(Integer)
    bag = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))  # Foreign key for User table
    driver_id = Column(Integer, ForeignKey('driver.id'), nullable=True)  # Foreign key for Driver table (optional)
    # driver_name = Column(String)
    # driver_plate = Column(String)
    # driver_rank = Column(Integer)
    cancelled = Column(Boolean, default=False)  # Boolean field for indicating ride cancellation
    completed = Column(Boolean, default=False)  # Boolean field for indicating ride completion
    user = relationship("User", back_populates="rides")
    driver = relationship("Driver", back_populates="rides")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)  # Foreign key for User table
    driver_id = Column(Integer, ForeignKey('driver.id'), nullable=True)  # Foreign key for Driver table (optional)
    user = relationship("User", back_populates="messages")
    driver = relationship("Driver", back_populates="messages")
    message = Column(String)
