from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Mock Statistics
        stats_layout = QVBoxLayout()
        stats_layout.addWidget(QLabel("Subjects: 0"))
        stats_layout.addWidget(QLabel("Materials: 0"))
        stats_layout.addWidget(QLabel("Knowledge Score: N/A"))
        stats_layout.addWidget(QLabel("Recent Assessments: 0"))
        
        layout.addWidget(title)
        layout.addLayout(stats_layout)
        layout.addStretch()
