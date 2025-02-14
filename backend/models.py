from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, Sequence, BigInteger, Date, ForeignKey, Float, Boolean


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, Sequence('user_id', metadata=Base.metadata), primary_key=True)
    email = Column(String, primary_key=True, unique=True)
    name = Column(String)
    bdate = Column(Date)
    approved = Column(Boolean, default=False)
    current_code = Column(String, nullable=True)


class TextField(Base):
    __tablename__ = "text_fields"

    id = Column(String, primary_key=True)
    description = Column(String)


class Texts(Base):
    __tablename__ = "texts"

    field_id = Column(String, ForeignKey(TextField.id, ondelete="CASCADE"), nullable=False, primary_key=True)
    language = Column(String, primary_key=True)
    text = Column(String)




