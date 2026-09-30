from typing import Protocol

from uni_helper.domain.subject import Subject


class SubjectNotFoundError(LookupError):
    """Raised when an operation targets a subject that no longer exists."""


class SubjectPersistenceError(RuntimeError):
    """Raised when subject data cannot be read or written."""


class SubjectRepository(Protocol):
    def list_all(self) -> list[Subject]:
        """Return all subjects in display order."""

    def add(self, subject: Subject) -> Subject:
        """Persist a new subject and return it with its assigned ID."""

    def update(self, subject: Subject) -> Subject | None:
        """Update an existing subject, or return None if it does not exist."""

    def delete(self, subject_id: int) -> bool:
        """Delete the subject and report whether it existed."""


class SubjectService:
    """Application use cases for managing subjects."""

    def __init__(self, repository: SubjectRepository) -> None:
        self._repository = repository

    def list_subjects(self) -> list[Subject]:
        """Return subjects for display."""
        return self._repository.list_all()

    def create_subject(self, name: str, description: str = "") -> Subject:
        """Validate and persist a new subject."""
        return self._repository.add(Subject(name=name, description=description))

    def update_subject(
        self,
        subject_id: int,
        name: str,
        description: str = "",
    ) -> Subject:
        """Validate and persist updates to an existing subject."""
        subject = Subject(name=name, description=description, id=subject_id)
        updated_subject = self._repository.update(subject)
        if updated_subject is None:
            raise SubjectNotFoundError(f"Subject {subject_id} was not found.")
        return updated_subject

    def delete_subject(self, subject_id: int) -> None:
        """Delete an existing subject or report that it was not found."""
        if not self._repository.delete(subject_id):
            raise SubjectNotFoundError(f"Subject {subject_id} was not found.")
