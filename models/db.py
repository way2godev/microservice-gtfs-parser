from pydantic import BaseModel

class DbModel(BaseModel):
    def save(self):
        raise NotImplementedError("This method must be implemented in the child class")
    
class Agency(DbModel):
    table_name = "agencies"
    name: str
    gtfs_agency_id: str | None = None
    gtfs_agency_name: str | None = None
    gtfs_agency_url: str | None = None
    gtfs_agency_timezone: str | None = None
    gtfs_agency_lang: str | None = None
    gtfs_agency_phone: str | None = None
    gtfs_agency_email: str | None = None
    
class Stop(DbModel):
    table_name = "stops"
    name: str
    description: str | None = None
    latitude: float
    longitude: float
    wheelchair_boarding: bool = False
    gtfs_stop_id: str
    gtfs_stop_code: str | None = None
    gtfs_location_type: int | None = None
    gtfs_stop_timezone: str | None = None
    
class Line(DbModel):
    table_name = "lines"
    name: str
    agency_id: int
    description: str | None = None
    route_type: int | None = None
    gtfs_route_id: str | None = None
    gtfs_route_short_name: str | None = None
    gtfs_route_long_name: str | None = None
    gtfs_route_url: str | None = None
    gtfs_route_color: str | None = None
    gtfs_route_text_color: str | None = None