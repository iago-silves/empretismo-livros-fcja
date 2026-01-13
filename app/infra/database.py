from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///biblioteca.db")
metadata = MetaData()

SessionLocal = sessionmaker(bind=engine)
