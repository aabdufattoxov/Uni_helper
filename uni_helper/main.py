import sys
from PySide6.QtWidgets import QApplication

from uni_helper.infrastructure.database.connection import DatabaseManager
from uni_helper.presentation.main_window import MainWindow

def main():
    # Initialize infrastructure
    db_manager = DatabaseManager()
    db_manager.init_db()
    
    # Initialize presentation
    app = QApplication(sys.argv)
    
    # We could inject dependencies into the main window here
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
