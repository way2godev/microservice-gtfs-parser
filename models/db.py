from pydantic import BaseModel
from db.connection import Connection
from utils.log import Logger

logger = Logger.get_logger()

class DbModel(BaseModel):
    def save(self):
        raise NotImplementedError("This method is not implemented in this class")
    
    def save_if_not_exists(self):
        raise NotImplementedError("This method is not implemented in this class")
    
class Agency(DbModel):
    table_name: str = "agencies"
    name: str
    gtfs_agency_id: str | None = None
    gtfs_agency_name: str | None = None
    gtfs_agency_url: str | None = None
    gtfs_agency_timezone: str | None = None
    gtfs_agency_lang: str | None = None
    gtfs_agency_phone: str | None = None
    gtfs_agency_email: str | None = None
    
class Stop(DbModel):
    table_name: str = "stops"
    name: str
    description: str | None = None
    latitude: float
    longitude: float
    wheelchair_boarding: bool | None = None
    gtfs_stop_id: str
    gtfs_stop_code: str | None = None
    gtfs_location_type: int | None = None
    gtfs_stop_timezone: str | None = None
    
    def get_by_gtfs_id(gtfs_stop_id):
        query = f"SELECT * FROM stops WHERE gtfs_stop_id LIKE '{gtfs_stop_id}'"
        db = Connection.get_cursor()
        db.execute(query)
        stop = db.fetchone()
        db.close()
        return stop
    
    def save(self):
        query = f"INSERT INTO stops (name, description, latitude, longitude, wheelchair_boarding, gtfs_stop_id, gtfs_stop_code, gtfs_location_type, gtfs_stop_timezone, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"
        db = Connection.get_cursor()
        db.execute(query, (self.name, self.description, self.latitude, self.longitude, self.wheelchair_boarding, self.gtfs_stop_id, self.gtfs_stop_code, self.gtfs_location_type, self.gtfs_stop_timezone))
        db.connection.commit()
        db.close()
    
    def save_if_not_exists(self):
        stop = Stop.get_by_gtfs_id(self.gtfs_stop_id)
        if not stop:
            logger.info(f"Saving stop {self.name}")
            self.save()
        else:
            logger.info(f"Stop {self.name} already exists in the database")

class Line(DbModel):
    table_name: str = "lines"
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