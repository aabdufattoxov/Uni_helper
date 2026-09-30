import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# Default SQLite database path
DEFAULT_DB_URL = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'uni_helper.db')}"

Base = declarative_base()

class DatabaseManager:
    def __init__(self, db_url=DEFAULT_DB_URL):
        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self):
        """Creates all tables."""
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_session(self):
        """Returns a new database session context."""
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
