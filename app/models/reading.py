from sqlalchemy import JSON, Column, Integer, String, TypeDecorator

from app.database import Base
from app.schemas.reading import Status


class StatusEnum(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(self):
        super().__init__(length=20)

    def process_bind_param(self, value, dialect):
        if value is not None:
            if isinstance(value, Status):
                return value.value
            elif isinstance(value, str):
                return value
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return Status(value)
        return value


class ReadingItemModel(Base):
    __tablename__ = "reading_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False, index=True)
    url = Column(String(2048), nullable=True)
    tags = Column(JSON, nullable=False, default=list)
    priority = Column(Integer, nullable=False, default=3)
    status = Column(StatusEnum(), nullable=False, default=Status.todo, index=True)
