from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from uni_helper.application.subject_service import SubjectPersistenceError
from uni_helper.domain.subject import Subject
from uni_helper.infrastructure.database.connection import DatabaseManager
from uni_helper.infrastructure.database.models import SubjectRecord


class SqlAlchemySubjectRepository:
    """Persist subjects using the application's managed database sessions."""

    def __init__(self, database: DatabaseManager) -> None:
        self._database = database

    def list_all(self) -> list[Subject]:
        """Return persisted subjects ordered by name and ID."""
        try:
            with self._database.session_scope() as session:
                records = session.scalars(
                    select(SubjectRecord).order_by(SubjectRecord.name, SubjectRecord.id)
                ).all()
                return [self._to_subject(record) for record in records]
        except SQLAlchemyError as error:
            raise SubjectPersistenceError("Could not load subjects.") from error

    def add(self, subject: Subject) -> Subject:
        """Insert a subject and return its database-assigned ID."""
        try:
            with self._database.session_scope() as session:
                record = SubjectRecord(
                    name=subject.name,
                    description=subject.description,
                )
                session.add(record)
                session.flush()
                return self._to_subject(record)
        except SQLAlchemyError as error:
            raise SubjectPersistenceError("Could not save the subject.") from error

    def update(self, subject: Subject) -> Subject | None:
        """Update a persisted subject or return None if it no longer exists."""
        if subject.id is None:
            raise ValueError("An existing subject ID is required for updates.")

        try:
            with self._database.session_scope() as session:
                record = session.get(SubjectRecord, subject.id)
                if record is None:
                    return None
                record.name = subject.name
                record.description = subject.description
                session.flush()
                return self._to_subject(record)
        except SQLAlchemyError as error:
            raise SubjectPersistenceError("Could not update the subject.") from error

    def delete(self, subject_id: int) -> bool:
        """Delete a persisted subject and return whether one was found."""
        try:
            with self._database.session_scope() as session:
                record = session.get(SubjectRecord, subject_id)
                if record is None:
                    return False
                session.delete(record)
                return True
        except SQLAlchemyError as error:
            raise SubjectPersistenceError("Could not delete the subject.") from error

    @staticmethod
    def _to_subject(record: SubjectRecord) -> Subject:
        return Subject(
            id=record.id,
            name=record.name,
            description=record.description,
        )
