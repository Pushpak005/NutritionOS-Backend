from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    Text,
    ForeignKey
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserProfile(Base):

    __tablename__ = "user_profile"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False
    )

    age = Column(Integer)

    gender = Column(Text)

    height = Column(Integer)

    weight = Column(Integer)