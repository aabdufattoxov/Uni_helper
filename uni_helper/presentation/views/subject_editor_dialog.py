from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from uni_helper.domain.subject import Subject


class SubjectEditorDialog(QDialog):
    def __init__(
        self,
        parent: QWidget | None = None,
        subject: Subject | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Edit Subject" if subject else "Add Subject")

        self.name_input = QLineEdit()
        self.name_input.setMaxLength(200)
        self.description_input = QTextEdit()
        self.description_input.setFixedHeight(100)

        if subject is not None:
            self.name_input.setText(subject.name)
            self.description_input.setPlainText(subject.description)

        form = QFormLayout()
        form.addRow("Name:", self.name_input)
        form.addRow("Description (optional):", self.description_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def subject_details(self) -> tuple[str, str]:
        return (
            self.name_input.text(),
            self.description_input.toPlainText(),
        )
