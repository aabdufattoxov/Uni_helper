from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from uni_helper.application.subject_service import (
    SubjectNotFoundError,
    SubjectPersistenceError,
    SubjectService,
)
from uni_helper.domain.subject import InvalidSubjectError, Subject
from uni_helper.presentation.views.subject_editor_dialog import SubjectEditorDialog


class SubjectsView(QWidget):
    def __init__(
        self,
        subject_service: SubjectService,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._subject_service = subject_service
        self._subjects: dict[int, Subject] = {}
        self._setup_ui()
        self.refresh_subjects()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        title = QLabel("Subjects")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.subject_list = QListWidget()
        self.subject_list.currentItemChanged.connect(self._update_action_state)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)

        self.add_button = QPushButton("Add Subject")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        actions = QHBoxLayout()
        actions.addWidget(self.add_button)
        actions.addWidget(self.edit_button)
        actions.addWidget(self.delete_button)
        actions.addStretch()

        layout.addWidget(title)
        layout.addWidget(self.subject_list)
        layout.addLayout(actions)
        layout.addWidget(self.status_label)

        self.add_button.clicked.connect(self._add_subject)
        self.edit_button.clicked.connect(self._edit_subject)
        self.delete_button.clicked.connect(self._delete_subject)

    def refresh_subjects(self) -> None:
        try:
            subjects = self._subject_service.list_subjects()
        except SubjectPersistenceError as error:
            self._subjects.clear()
            self.subject_list.clear()
            self.status_label.setText(str(error))
            self._update_action_state()
            return

        self._subjects = {
            subject.id: subject for subject in subjects if subject.id is not None
        }
        self.subject_list.clear()
        for subject in subjects:
            item = QListWidgetItem(subject.name)
            if subject.description:
                item.setToolTip(subject.description)
            item.setData(Qt.ItemDataRole.UserRole, subject.id)
            self.subject_list.addItem(item)

        if subjects:
            self.status_label.clear()
        else:
            self.status_label.setText("No subjects yet. Add a subject to get started.")
        self._update_action_state()

    def _add_subject(self) -> None:
        dialog = SubjectEditorDialog(self)
        if dialog.exec() != SubjectEditorDialog.DialogCode.Accepted:
            return

        name, description = dialog.subject_details()
        try:
            subject = self._subject_service.create_subject(name, description)
        except (InvalidSubjectError, SubjectPersistenceError) as error:
            self.status_label.setText(str(error))
            return

        self.refresh_subjects()
        self._select_subject(subject.id)

    def _edit_subject(self) -> None:
        subject = self._selected_subject()
        if subject is None or subject.id is None:
            self.status_label.setText("Select a subject to edit.")
            return

        dialog = SubjectEditorDialog(self, subject)
        if dialog.exec() != SubjectEditorDialog.DialogCode.Accepted:
            return

        name, description = dialog.subject_details()
        try:
            updated_subject = self._subject_service.update_subject(
                subject.id,
                name,
                description,
            )
        except (
            InvalidSubjectError,
            SubjectNotFoundError,
            SubjectPersistenceError,
        ) as error:
            self.refresh_subjects()
            self.status_label.setText(str(error))
            return

        self.refresh_subjects()
        self._select_subject(updated_subject.id)

    def _delete_subject(self) -> None:
        subject = self._selected_subject()
        if subject is None or subject.id is None:
            self.status_label.setText("Select a subject to delete.")
            return

        confirmation = QMessageBox.question(
            self,
            "Delete Subject",
            f'Delete "{subject.name}"? This action cannot be undone.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirmation != QMessageBox.StandardButton.Yes:
            return

        try:
            self._subject_service.delete_subject(subject.id)
        except (SubjectNotFoundError, SubjectPersistenceError) as error:
            self.refresh_subjects()
            self.status_label.setText(str(error))
            return

        self.refresh_subjects()

    def _selected_subject(self) -> Subject | None:
        item = self.subject_list.currentItem()
        if item is None:
            return None
        subject_id = item.data(Qt.ItemDataRole.UserRole)
        return self._subjects.get(subject_id)

    def _select_subject(self, subject_id: int | None) -> None:
        if subject_id is None:
            return
        for index in range(self.subject_list.count()):
            item = self.subject_list.item(index)
            if item.data(Qt.ItemDataRole.UserRole) == subject_id:
                self.subject_list.setCurrentItem(item)
                return

    def _update_action_state(self, *_args) -> None:
        has_selection = self.subject_list.currentItem() is not None
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
