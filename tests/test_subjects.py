import pytest

from uni_helper.application.subject_service import (
    SubjectNotFoundError,
    SubjectService,
)
from uni_helper.domain.subject import InvalidSubjectError
from uni_helper.infrastructure.database.connection import DatabaseManager
from uni_helper.infrastructure.database.subject_repository import (
    SqlAlchemySubjectRepository,
)


def test_subject_crud_persists_with_normalized_fields(tmp_path):
    database = DatabaseManager(f"sqlite:///{tmp_path / 'subjects.db'}")
    database.init_db()
    service = SubjectService(SqlAlchemySubjectRepository(database))

    try:
        assert service.list_subjects() == []

        subject = service.create_subject("  Data Structures  ", "  Trees and graphs  ")
        assert subject.id is not None
        assert subject.name == "Data Structures"
        assert subject.description == "Trees and graphs"
        assert service.list_subjects() == [subject]

        updated = service.update_subject(
            subject.id,
            "Algorithms",
            "Sorting and searching",
        )
        assert updated.id == subject.id
        assert updated.name == "Algorithms"
        assert service.list_subjects() == [updated]

        service.delete_subject(subject.id)
        assert service.list_subjects() == []
        with pytest.raises(SubjectNotFoundError):
            service.delete_subject(subject.id)
    finally:
        database.close()


@pytest.mark.parametrize("name", ["", "   ", "x" * 201])
def test_subject_rejects_invalid_names(tmp_path, name):
    database = DatabaseManager(f"sqlite:///{tmp_path / 'subjects.db'}")
    database.init_db()
    service = SubjectService(SqlAlchemySubjectRepository(database))

    try:
        with pytest.raises(InvalidSubjectError):
            service.create_subject(name)
        assert service.list_subjects() == []
    finally:
        database.close()


def test_update_missing_subject_raises_not_found(tmp_path):
    database = DatabaseManager(f"sqlite:///{tmp_path / 'subjects.db'}")
    database.init_db()
    service = SubjectService(SqlAlchemySubjectRepository(database))

    try:
        with pytest.raises(SubjectNotFoundError):
            service.update_subject(999, "Missing")
    finally:
        database.close()
