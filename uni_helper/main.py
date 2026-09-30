import sys
from PySide6.QtWidgets import QApplication, QMessageBox

from uni_helper.infrastructure.database.connection import DatabaseManager
from uni_helper.presentation.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    try:
        # Initialize infrastructure
        db_manager = DatabaseManager()
        db_manager.init_db()
    except Exception as e:
        QMessageBox.critical(None, "Startup Error", f"Failed to initialize database:\n{e}")
        sys.exit(1)
    
    # We could inject dependencies into the main window here
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
