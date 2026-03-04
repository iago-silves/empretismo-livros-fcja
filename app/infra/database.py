from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine(
    "sqlite:///biblioteca.db",
    echo=True,                 
    future=True
)

@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

metadata = MetaData()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()