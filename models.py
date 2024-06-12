from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Text, Numeric, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

DATABASE_URI = 'mysql+pymysql://root:root@localhost/{your_database_name}'


# Create engine
engine = create_engine(DATABASE_URI)

# Create a base class for declarative class definitions
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    manufacturer = Column(Text, nullable=False)
    price = Column(Numeric(18, 2), nullable=False)
    tax = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False, nullable=False)


class KawaBikeURL(Base):
    __tablename__ = 'kawa_urls'
    id = Column(Integer, primary_key=True)
    url = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False, nullable=False)


# class {OTHER MODELS}

# Create tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
