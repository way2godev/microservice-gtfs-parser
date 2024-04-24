from dataclasses import dataclass
from pydantic import BaseModel
import random

class Agency(BaseModel):
    id: int = random.randint(1, 100_000)
    name: str
    raw_id: int | None = None
    url: str | None = None
    phone_number: str | int | None = None

class Line(BaseModel):
    id: str
    name: str = ""
    agency: Agency


class Stop(BaseModel):
    id: int = 0
    name: str
    latitude: float
    longitude: float
    raw_renfe_code: int | None = None
    address: str | None = None
    city: str | None = None
    postal_code: int | None = None
    province: str | None = None
    country: str | None = None

class LineVariant(BaseModel):
    id: int = 0
    name: str = ""
    line: Line
    origin_stop: Stop
    destination_stop: Stop

class Schedule(BaseModel):
    id: int = 0
    line: LineVariant
    days: str = "1111111"

class ScheduleStop(BaseModel):
    id: int = 0
    schedule: Schedule
    stop: Stop
    order: int