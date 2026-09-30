from dataclasses import dataclass


class InvalidSubjectError(ValueError):
    """Raised when subject details do not meet domain requirements."""


@dataclass(frozen=True)
class Subject:
    """A course subject managed by the student."""

    name: str
    description: str = ""
    id: int | None = None

    def __post_init__(self) -> None:
        name = self.name.strip()
        if not name:
            raise InvalidSubjectError("A subject name is required.")
        if len(name) > 200:
            raise InvalidSubjectError("A subject name cannot exceed 200 characters.")
        if self.id is not None and self.id < 1:
            raise InvalidSubjectError("A subject ID must be a positive integer.")

        object.__setattr__(self, "name", name)
        object.__setattr__(self, "description", self.description.strip())
