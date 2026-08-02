from sqlalchemy import (
    Column,
    BigInteger,
    Text,
    Numeric,
    TIMESTAMP
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)

    created_at = Column(TIMESTAMP)

    # Basic Account
    name = Column(Text)
    email = Column(Text, unique=True, index=True)
    password_hash = Column(Text)

    # Personal
    age = Column(BigInteger)
    gender = Column(Text)

    # Body Metrics
    height_cm = Column(Numeric)
    weight_kg = Column(Numeric)
    bmi = Column(Numeric)
    target_weight = Column(Numeric)

    # Goals
    goal = Column(Text)

    # Lifestyle
    activity_level = Column(Text)
    daily_budget = Column(Numeric)

    # Nutrition Targets
    daily_calories = Column(Numeric)
    daily_protein = Column(Numeric)
    daily_carbs = Column(Numeric)
    daily_fat = Column(Numeric)
    daily_fiber = Column(Numeric)

    # Health
    allergies = Column(Text)
    health_conditions = Column(Text)

    # Preferences
    diet_preferences = Column(Text)