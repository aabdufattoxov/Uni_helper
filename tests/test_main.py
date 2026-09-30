from unittest.mock import Mock

import pytest
from sqlalchemy.exc import SQLAlchemyError

import uni_helper.main as application


@pytest.mark.parametrize(
    "startup_error",
    [
        OSError("database is unavailable"),
        SQLAlchemyError("database initialization failed"),
    ],
)
def test_database_startup_error_is_reported(monkeypatch, startup_error):
    app = Mock()
    database_manager = Mock()
    database_manager.init_db.side_effect = startup_error
    message_box = Mock()

    monkeypatch.setattr(application, "QApplication", Mock(return_value=app))
    monkeypatch.setattr(
        application,
        "DatabaseManager",
        Mock(return_value=database_manager),
    )
    monkeypatch.setattr(application, "QMessageBox", message_box)

    result = application.main()

    assert result == 1
    message_box.critical.assert_called_once()
    app.exec.assert_not_called()
    database_manager.close.assert_called_once()


def test_successful_startup_shows_window_and_returns_exit_code(monkeypatch):
    app = Mock()
    app.exec.return_value = 0
    database_manager = Mock()
    window = Mock()

    monkeypatch.setattr(application, "QApplication", Mock(return_value=app))
    monkeypatch.setattr(
        application,
        "DatabaseManager",
        Mock(return_value=database_manager),
    )
    monkeypatch.setattr(application, "MainWindow", Mock(return_value=window))

    result = application.main()

    assert result == 0
    database_manager.init_db.assert_called_once()
    window.show.assert_called_once()
    app.exec.assert_called_once()
    database_manager.close.assert_called_once()
