'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 10/01/2026
Ending //

'''
# Installing the necessary libraries
import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey


# Creating a base class for models
class Base(DeclarativeBase):
    pass


# Defining the 'catalog' table structure
class Catalog(Base):
    __tablename__ = 'catalog'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str]
    photo1: Mapped[str]
    photo2: Mapped[str]
    photo3: Mapped[str]
    total_area: Mapped[float]
    living_area: Mapped[float]
    kitchen_area: Mapped[float]
    description: Mapped[str]
    address: Mapped[str]
    price: Mapped[float]
    category: Mapped[str]
    bookings: Mapped[list["Booking"]] = relationship(back_populates="apartment", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship(back_populates="apartment", cascade="all, delete-orphan")


# Defining the 'users' table structure
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone: Mapped[str]
    bookings: Mapped[list["Booking"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user", cascade="all, delete-orphan")


# Defining the 'bookings' table structure
class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    apartment_id: Mapped[int] = mapped_column(ForeignKey('catalog.id', ondelete="CASCADE"))
    start_date: Mapped[datetime.date]
    end_date: Mapped[datetime.date]
    rent_days: Mapped[int]
    total_price: Mapped[float]
    user: Mapped["User"] = relationship(back_populates="bookings")
    apartment: Mapped["Catalog"] = relationship(back_populates="bookings")


# Defining the 'reviews' table structure
class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    apartment_id: Mapped[int] = mapped_column(ForeignKey('catalog.id', ondelete="CASCADE"))
    review_text: Mapped[str]
    sentiment_label: Mapped[str]
    sentiment_score: Mapped[float]
    date: Mapped[datetime.date] = mapped_column(default=datetime.date.today)
    user: Mapped["User"] = relationship(back_populates="reviews")
    apartment: Mapped["Catalog"] = relationship(back_populates="reviews")
