from enum import Enum

from pydantic import BaseModel, HttpUrl, conint, constr


class Status(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


TitleStr = constr(min_length=1, max_length=120, strip_whitespace=True)
TagStr = constr(min_length=1, max_length=24, strip_whitespace=True)
PriorityInt = conint(ge=1, le=5)


class ReadingItemBase(BaseModel):
    title: TitleStr
    url: HttpUrl | None = None
    tags: list[TagStr] = []
    priority: PriorityInt = 3


class ReadingItemCreate(ReadingItemBase):
    pass


class ReadingItemUpdate(BaseModel):
    title: TitleStr | None = None
    url: HttpUrl | None = None
    tags: list[TagStr] | None = None
    priority: PriorityInt | None = None
    status: Status | None = None


class ReadingItem(ReadingItemBase):
    id: int
    status: Status = Status.todo
