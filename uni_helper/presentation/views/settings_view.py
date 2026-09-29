from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit
from PySide6.QtCore import Qt

class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        form_layout = QFormLayout()
        
        # Mock Settings for now
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter Gemini API Key")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("Gemini API Key:", self.api_key_input)
        
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addStretch()
