from enum import Enum
from typing import List, Optional

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
    url: Optional[HttpUrl] = None
    tags: List[TagStr] = []
    priority: PriorityInt = 3


class ReadingItemCreate(ReadingItemBase):
    pass


class ReadingItemUpdate(BaseModel):
    title: Optional[TitleStr] = None
    url: Optional[HttpUrl] = None
    tags: Optional[List[TagStr]] = None
    priority: Optional[PriorityInt] = None
    status: Optional[Status] = None


class ReadingItem(ReadingItemBase):
    id: int
    status: Status = Status.todo
