import pytest
from PySide6.QtWidgets import QApplication
from uni_helper.presentation.main_window import MainWindow

def test_main_window_initialization(qtbot):
    # qtbot automatically handles the QApplication
    window = MainWindow()
    qtbot.addWidget(window)
    
    assert window.windowTitle() == "Uni Helper"
    
    # Check that initial view is Dashboard
    assert window.content_area.currentIndex() == 0
    
    # Check switching to settings
    window.switch_view(1)
    assert window.content_area.currentIndex() == 1
