from os import truncate
from typing import List
from fastapi import APIRouter
from domain.Factory import Factory
from model.event import Event, EventTable
from domain.eventSort import sort_date

router = APIRouter()
apipath = "/api/v01"


@router.post(f"{apipath}/event")
def get_event(data: Event):
    res: List[EventTable] = []
    for target in data.target:
        com = Factory(target).strategy
        res += com.get_event(data)
    return sort_date(res)[:data.limit]
