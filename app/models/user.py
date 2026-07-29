from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)

    name = Column(Text)

    email = Column(Text, unique=True, index=True)

    password_hash = Column(Text)