from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from config_data.config import Config

# Database URI configuration from the Config class
DATABASE_URI = Config.DATABASE_URI

# Base class for declarative class definitions
Base = declarative_base()


class VacancyCount(Base):
    """
    Database model representing a vacancy count record.

    Attributes:
        id (int): Primary key, unique identifier for each record.
        datetime (datetime): The date and time when the record was created.
        count (int): The number of vacancies recorded.
        change (int): The change in the number of vacancies compared to the previous record.
    """

    __tablename__ = 'vacancy_counts'

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    count = Column(Integer)
    change = Column(Integer, default=0)


# Create a new SQLAlchemy engine instance
engine = create_engine(DATABASE_URI)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initializes the database by creating all tables defined in the metadata.
    """
    Base.metadata.create_all(bind=engine)
