from typing import Dict, List, Optional, Union
from pydantic import BaseModel


class Card(BaseModel):
    id: int
    title: str
    description: str
    stackId: int
    type: str
    lastModified: int
    lastEditor: Optional[str] = None
    createdAt: int
    labels: Optional[List] = None
    assignedUsers: List
    attachments: Optional[List] = None
    attachmentCount: int
    owner: Optional[Union[str, Dict]]
    order: int
    archived: bool
    done: Optional[bool] = None
    duedate: Optional[int] = None
    deletedAt: int
    commentsUnread: int
    commentsCount: int
    ETag: str
    overdue: int
    referenceData: Optional[str] = None


class Stack(BaseModel):
    id: int
    title: str
    boardId: int
    lastModified: int
    cards: list[Card]
    order: int
    ETag: str
