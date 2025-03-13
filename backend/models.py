from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, Sequence, BigInteger, DateTime, ForeignKey, Float, Boolean, Date


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, Sequence('user_id', metadata=Base.metadata), primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    bdate = Column(Date)
    approved = Column(Boolean, default=False)
    current_code = Column(String, nullable=True)
    registration_date = Column(DateTime)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True)
    description = Column(String)


class SubscriptionInterval(Base):
    __tablename__ = "subscriptions_intervals"

    subscription_id = Column(String, ForeignKey(Subscription.id, ondelete="CASCADE"), nullable=False, primary_key=True)
    months = Column(Integer, primary_key=True)
    cost = Column(Integer)


class UserHasSubscription(Base):
    __tablename__ = "user_has_subscription"

    user_id = Column(BigInteger, ForeignKey(User.id, ondelete="CASCADE"), nullable=False, primary_key=True, index=True)
    subscription = Column(String, ForeignKey(Subscription.id, ondelete="CASCADE"), nullable=False, primary_key=True, index=True)
    expires = Column(DateTime)


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(BigInteger, Sequence('invoice_id', metadata=Base.metadata), primary_key=True, index=True)
    from_user = Column(BigInteger, ForeignKey(User.id, ondelete="CASCADE"), nullable=False, primary_key=True, index=True)
    cost = Column(Integer)
    succeed = Column(Boolean)


class TextField(Base):
    __tablename__ = "text_fields"

    id = Column(String, primary_key=True)
    description = Column(String)


class GeneralTexts(Base):
    __tablename__ = "general_texts"

    field_id = Column(String, ForeignKey(TextField.id, ondelete="CASCADE"), nullable=False, primary_key=True)
    language = Column(String, primary_key=True)
    text = Column(String)


class SubscriptionTexts(Base):
    __tablename__ = "subscription_texts"

    field = Column(String, primary_key=True)
    number = Column(BigInteger, primary_key=True)
    language = Column(String, primary_key=True)
    subscription_id = Column(String, ForeignKey(Subscription.id, ondelete="CASCADE"), nullable=False, primary_key=True)
    text = Column(String)


class Colors(Base):
    __tablename__ = "colors"

    number = Column(Integer, primary_key=True)
    hex = Column(String)
