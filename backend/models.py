from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, Sequence, BigInteger, Date, ForeignKey, Float, Boolean


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, Sequence('user_id', metadata=Base.metadata), primary_key=True)
    email = Column(String, unique=True)
    name = Column(String)
    bdate = Column(Date)
    approved = Column(Boolean, default=False)
    current_code = Column(String, nullable=True)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, Sequence('subscription_id', metadata=Base.metadata), primary_key=True)
    description = Column(String)


class UserHasSubscription(Base):
    __tablename__ = "user_has_subscription"

    user_id = Column(BigInteger, ForeignKey(User.id, ondelete="CASCADE"), nullable=False, primary_key=True)
    subscription = Column(String, ForeignKey(Subscription.id, ondelete="CASCADE"), nullable=False, primary_key=True)
    expires = Column(Date, nullable=False)


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

    number = Column(BigInteger, primary_key=True)
    language = Column(String, primary_key=True)
    subscription = Column(String, ForeignKey(Subscription.id, ondelete="CASCADE"), nullable=False, primary_key=True)
    text = Column(String)
