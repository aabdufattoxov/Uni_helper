from unittest.mock import Mock

import pytest
from sqlalchemy import inspect

from uni_helper.infrastructure.database.connection import DatabaseManager


def test_database_initialization_uses_user_data_directory(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))

    db_manager = DatabaseManager()
    db_file = tmp_path / "Uni_helper" / "uni_helper.db"

    db_manager.init_db()

    assert db_manager.engine.url.database == str(db_file)
    assert db_file.exists()
    assert "subjects" in inspect(db_manager.engine).get_table_names()
    db_manager.engine.dispose()


def test_default_database_requires_local_app_data(monkeypatch):
    monkeypatch.delenv("LOCALAPPDATA", raising=False)

    with pytest.raises(OSError, match="LOCALAPPDATA"):
        DatabaseManager()


def test_session_scope_commits_and_closes(tmp_path):
    db_manager = DatabaseManager(f"sqlite:///{tmp_path / 'test.db'}")
    session = Mock()
    db_manager.SessionLocal = Mock(return_value=session)

    with db_manager.session_scope() as yielded_session:
        assert yielded_session is session

    session.commit.assert_called_once()
    session.rollback.assert_not_called()
    session.close.assert_called_once()


def test_session_scope_rolls_back_and_closes_on_error(tmp_path):
    db_manager = DatabaseManager(f"sqlite:///{tmp_path / 'test.db'}")
    session = Mock()
    db_manager.SessionLocal = Mock(return_value=session)

    with pytest.raises(ValueError, match="operation failed"):
        with db_manager.session_scope():
            raise ValueError("operation failed")

    session.commit.assert_not_called()
    session.rollback.assert_called_once()
    session.close.assert_called_once()


def test_session_scope_rolls_back_and_closes_when_commit_fails(tmp_path):
    db_manager = DatabaseManager(f"sqlite:///{tmp_path / 'test.db'}")
    session = Mock()
    session.commit.side_effect = RuntimeError("commit failed")
    db_manager.SessionLocal = Mock(return_value=session)

    with pytest.raises(RuntimeError, match="commit failed"):
        with db_manager.session_scope():
            pass

    session.commit.assert_called_once()
    session.rollback.assert_called_once()
    session.close.assert_called_once()
