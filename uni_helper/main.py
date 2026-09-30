import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from sqlalchemy.exc import SQLAlchemyError

from uni_helper.infrastructure.database.connection import DatabaseManager
from uni_helper.presentation.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)

    db_manager = None
    try:
        db_manager = DatabaseManager()
        db_manager.init_db()
    except (OSError, SQLAlchemyError) as error:
        if db_manager is not None:
            db_manager.close()
        QMessageBox.critical(
            None,
            "Startup Error",
            f"Uni Helper could not initialize its database: {error}",
        )
        return 1

    window = MainWindow()
    window.show()
    try:
        return app.exec()
    finally:
        if db_manager is not None:
            db_manager.close()


if __name__ == "__main__":
    sys.exit(main())
