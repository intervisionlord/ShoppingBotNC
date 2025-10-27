from pydantic import BaseModel
from typing import Dict, List, Optional, Union

# TODO: Референсные данные - удалить после тестов
# "title": "Board title",
# "owner": {
#     "primaryKey": "admin",
#     "uid": "admin",
#     "displayname": "Administrator"
# },
# "color": "ff0000",
# "archived": false,
# "labels": [],
# "acl": [],
# "permissions": {
#     "PERMISSION_READ": true,
#     "PERMISSION_EDIT": true,
#     "PERMISSION_MANAGE": true,
#     "PERMISSION_SHARE": true
# },
# "users": [],
# "shared": 0,
# "deletedAt": 0,
# "id": 10,
# "lastModified": 1586269585,
# "settings": {
#     "notify-due": "off",
#     "calendar": true


class Owner(BaseModel):
    primaryKey: str
    uid: str
    displayname: str


class Permissions(BaseModel):
    PERMISSION_READ: bool
    PERMISSION_EDIT: bool
    PERMISSION_MANAGE: bool
    PERMISSION_SHARE: bool


class Settings(BaseModel):
    notify_due: str
    calendar: bool


class ModelBoard(BaseModel):
    title: str
    owner: Owner
    color: str
    archived: bool
    labels: List[str]
    acl: List[Dict]
    permissions: Permissions
    users: List[Dict]
    shared: int
    deletedAt: int
    id: int
    lastModified: int
    settings: Optional[Union[Settings, List]] = None
