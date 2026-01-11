'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 10/01/2026
Ending //

'''
# Installing the necessary libraries
import datetime
from src.db.database import session_factory
from src.db.models import User, Catalog, Booking, Review
from src.nlp.sentiment_analyzer import analyze_review


# Adding the user to the database
def insert_user_data(user_id, first_name, last_name, phone):
    with session_factory() as session:
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
        else:
            user = User(user_id=user_id, first_name=first_name, last_name=last_name, phone=phone)
            session.add(user)
        session.commit()


# Check if there is a user in the database
def check_user_exists(session, user_id):
    return session.query(User).filter_by(user_id=user_id).first() is not None


def get_catalog_data():
    with session_factory() as session:
        return session.query(Catalog).all()


def get_catalog_by_category(category):
    with session_factory() as session:
        return session.query(Catalog).filter_by(category=category).all()


# Checking if the apartment is available
def is_apartment_available(apartment_id, start_date, end_date):
    with session_factory() as session:
        conflicts = session.query(Booking).filter(
            Booking.apartment_id == apartment_id,
            ((Booking.start_date <= start_date) & (Booking.end_date >= start_date)) |
            ((Booking.start_date <= end_date) & (Booking.end_date >= end_date))
        ).first()
        return conflicts is None


# Inserts a new booking record
def insert_booking_data(user_id, apartment_id, start_date, rent_days, total_price):
    end_date = start_date + datetime.timedelta(days=rent_days)
    with session_factory() as session:
        booking = Booking(
            user_id=user_id,
            apartment_id=apartment_id,
            start_date=start_date,
            end_date=end_date,
            rent_days=rent_days,
            total_price=total_price
        )
        session.add(booking)
        session.commit()


# Retrieves all booking records along with user and apartment details
def get_bookings():
    with session_factory() as session:
        return session.query(Booking).join(User).join(Catalog).all()


# Insert a new record into the 'catalog' table using the provided data
def insert_apartment_data(data):
    with session_factory() as session:
        apartment = Catalog(
            date=data[0],
            photo1=data[1],
            photo2=data[2],
            photo3=data[3],
            total_area=data[4],
            living_area=data[5],
            kitchen_area=data[6],
            description=data[7],
            address=data[8],
            price=data[9],
            category=data[10]
        )
        session.add(apartment)
        session.commit()


# Delete apartment data in the 'catalog' table by the specified ID
def delete_apartment_data(apartment_id):
    with session_factory() as session:
        apartment = session.query(Catalog).get(apartment_id)
        if apartment:
            session.delete(apartment)
            session.commit()


# Updates apartment data in the 'catalog' table by the specified ID
def update_apartment_data(apartment_id, photo1, photo2, photo3, total_area, living_area, kitchen_area, description, address, price, category):
    with session_factory() as session:
        apartment = session.query(Catalog).get(apartment_id)
        if apartment:
            apartment.photo1 = photo1
            apartment.photo2 = photo2
            apartment.photo3 = photo3
            apartment.total_area = total_area
            apartment.living_area = living_area
            apartment.kitchen_area = kitchen_area
            apartment.description = description
            apartment.address = address
            apartment.price = price
            apartment.category = category
            session.commit()


def insert_review(user_id, apartment_id, review_text):
    analysis = analyze_review(review_text)
    with session_factory() as session:
        review = Review(
            user_id=user_id,
            apartment_id=apartment_id,
            review_text=review_text,
            sentiment_label=analysis["label"],
            sentiment_score=analysis["score"]
        )
        session.add(review)
        session.commit()


# Retrieves a list of all reviews from the database, sorted by date (new first)
def get_reviews():
    with session_factory() as session:
        return session.query(Review).order_by(Review.date.desc()).all()
