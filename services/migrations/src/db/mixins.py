from sqlmodel import Field
from uuid import UUID, uuid4


class UUIDMixin:
    id: UUID = Field(primary_key=True, default_factory=uuid4)
