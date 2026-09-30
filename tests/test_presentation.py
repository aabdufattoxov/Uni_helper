from PySide6.QtWidgets import QMessageBox, QDialog

import uni_helper.presentation.views.subjects_view as subjects_view_module
from uni_helper.application.subject_service import SubjectService
from uni_helper.infrastructure.database.connection import DatabaseManager
from uni_helper.infrastructure.database.subject_repository import (
    SqlAlchemySubjectRepository,
)
from uni_helper.presentation.main_window import MainWindow


def test_main_window_navigation_and_subject_crud(tmp_path, monkeypatch, qtbot):
    database = DatabaseManager(f"sqlite:///{tmp_path / 'subjects.db'}")
    database.init_db()
    subject_service = SubjectService(SqlAlchemySubjectRepository(database))
    window = MainWindow(subject_service)
    qtbot.addWidget(window)

    class AcceptedSubjectDialog:
        DialogCode = QDialog.DialogCode
        details = iter(
            [
                ("Algorithms", "Core problem-solving course"),
                ("Advanced Algorithms", "Core problem-solving course"),
            ]
        )

        def __init__(self, *_args, **_kwargs):
            self._details = next(self.details)

        def exec(self):
            return self.DialogCode.Accepted

        def subject_details(self):
            return self._details

    monkeypatch.setattr(
        subjects_view_module,
        "SubjectEditorDialog",
        AcceptedSubjectDialog,
    )
    monkeypatch.setattr(
        subjects_view_module.QMessageBox,
        "question",
        lambda *_args: QMessageBox.StandardButton.Yes,
    )

    try:
        assert window.content_area.currentIndex() == 0

        window.btn_subjects.click()
        assert window.content_area.currentIndex() == 1

        view = window.subjects_view
        assert view.subject_list.count() == 0
        assert "No subjects yet" in view.status_label.text()

        view.add_button.click()
        assert view.subject_list.count() == 1
        assert view.subject_list.item(0).text() == "Algorithms"

        view.edit_button.click()
        assert view.subject_list.item(0).text() == "Advanced Algorithms"

        view.delete_button.click()
        assert view.subject_list.count() == 0
        assert subject_service.list_subjects() == []

        window.btn_settings.click()
        assert window.content_area.currentIndex() == 2
    finally:
        database.close()
