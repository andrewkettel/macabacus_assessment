from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field, UUID4
from enum import Enum
from datetime import datetime


class StatusEnum(Enum):
    ToDo = "todo"
    InProgress = "in_progress"
    Done = "done"


class Task(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    title: str
    status: StatusEnum
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Complete the project",
                "status": "todo",
            }
        }
    )
