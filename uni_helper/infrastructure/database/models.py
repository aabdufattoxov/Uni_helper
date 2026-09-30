from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from uni_helper.infrastructure.database.connection import Base


class SubjectRecord(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
