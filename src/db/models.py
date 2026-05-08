import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey, Date, UniqueConstraint
from pgvector.sqlalchemy import Vector

# Creating a base class for models
class Base(DeclarativeBase):
    pass


# Catalog table
class Catalog(Base):
    __tablename__ = 'catalog'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
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


# Users table
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone: Mapped[str]
    bookings: Mapped[list["Booking"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user", cascade="all, delete-orphan")


# Bookings table
class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey('catalog.id', ondelete="CASCADE"), index=True)
    start_date: Mapped[datetime.date]
    end_date: Mapped[datetime.date]
    rent_days: Mapped[int]
    total_price: Mapped[float]
    user: Mapped["User"] = relationship(back_populates="bookings")
    apartment: Mapped["Catalog"] = relationship(back_populates="bookings")


# Reviews table
class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey('catalog.id', ondelete="CASCADE"), index=True)
    review_text: Mapped[str]
    sentiment_label: Mapped[str]
    sentiment_score: Mapped[float]
    date: Mapped[datetime.date] = mapped_column(default=datetime.date.today)
    user: Mapped["User"] = relationship(back_populates="reviews")
    apartment: Mapped["Catalog"] = relationship(back_populates="reviews")

# Reservation draft table
class ReservationDraft(Base):
    __tablename__ = 'reservation_drafts'
    __table_args__ = (
        UniqueConstraint('user_id', 'apartment_id', 'start_date', 'end_date'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'),index=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey('catalog.id', ondelete='CASCADE'), index=True)
    start_date: Mapped[datetime.date]
    end_date: Mapped[datetime.date]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    user: Mapped["User"] = relationship(backref="reservation_drafts")
    apartment: Mapped["Catalog"] = relationship(backref="reservation_drafts")
    services: Mapped[list["ReservationDraftService"]]

# Service table
class Service(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]

# Reservation draft service table
class ReservationDraftService(Base):
    __tablename__ = 'reservation_draft_services'
    __table_args__ = (
        UniqueConstraint('reservation_draft_id', 'service_id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    reservation_draft_id: Mapped[int] = mapped_column(ForeignKey('reservation_drafts.id', ondelete='CASCADE'), index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey('services.id', ondelete='CASCADE'), index=True)
    reservation_draft: Mapped["ReservationDraft"] = relationship(backref="services")
    service: Mapped["Service"] = relationship(backref="reservation_drafts")

# Document chunks table
class DocumentChunk(Base):
    __tablename__ = 'document_chunks'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    embedding: Mapped[Vector] = mapped_column(Vector(384))
