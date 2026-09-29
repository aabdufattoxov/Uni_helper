from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget
from PySide6.QtCore import Qt

from uni_helper.presentation.views.dashboard_view import DashboardView
from uni_helper.presentation.views.settings_view import SettingsView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Uni Helper")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(200)
        sidebar_widget.setStyleSheet("background-color: #2c3e50; color: white;")
        sidebar_layout = QVBoxLayout(sidebar_widget)
        
        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_settings = QPushButton("Settings")
        
        # Simple styling for buttons
        btn_style = """
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #3d566e;
            }
        """
        self.btn_dashboard.setStyleSheet(btn_style)
        self.btn_settings.setStyleSheet(btn_style)
        
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addStretch()
        
        # Main content area
        self.content_area = QStackedWidget()
        
        # Views
        self.dashboard_view = DashboardView()
        self.settings_view = SettingsView()
        
        self.content_area.addWidget(self.dashboard_view)
        self.content_area.addWidget(self.settings_view)
        
        # Layout assembly
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.content_area)
        
        # Connections
        self.btn_dashboard.clicked.connect(lambda: self.switch_view(0))
        self.btn_settings.clicked.connect(lambda: self.switch_view(1))
        
        # Init
        self.switch_view(0)

    def switch_view(self, index):
        self.content_area.setCurrentIndex(index)
