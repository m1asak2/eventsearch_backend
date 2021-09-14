from typing import List
from pydantic import BaseModel


class Event(BaseModel):
    keyword: List[str]
    address: List[str]
    start_from: str
    start_to: str
    limit: int
    target: List[str]


class EventTable(BaseModel):
    day: str
    time: str
    address: str
    title: str
    group: str
    img: str
    link: str
