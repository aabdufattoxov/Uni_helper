import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, declarative_base, sessionmaker


Base = declarative_base()


def _default_database_url() -> URL:
    """Return a SQLite URL in the current Windows user's writable data directory."""
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        raise OSError("The LOCALAPPDATA environment variable is not set.")

    data_directory = Path(local_app_data) / "Uni_helper"
    data_directory.mkdir(parents=True, exist_ok=True)
    return URL.create("sqlite", database=str(data_directory / "uni_helper.db"))


class DatabaseManager:
    def __init__(self, db_url: str | URL | None = None) -> None:
        if db_url is None:
            db_url = _default_database_url()
        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

    def init_db(self) -> None:
        """Creates all tables."""
        Base.metadata.create_all(bind=self.engine)

    def close(self) -> None:
        """Dispose of the engine's pooled database connections."""
        self.engine.dispose()

    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        """Yield a session, committing on success and rolling back on failure."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
