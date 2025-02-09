from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass

# using sqlite for testing
engine = create_engine(url="sqlite:///contacts.db")
DbSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    """get the db session as generator."""
    db = DbSession()

    try:
        yield db
    finally:
        db.close()

