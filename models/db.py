from pydantic import BaseModel
from db.connection import Connection
from utils.log import Logger
from datetime import datetime

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
    gtfs_agency_url: str | None = None
    gtfs_agency_timezone: str | None = None
    gtfs_agency_lang: str | None = None
    gtfs_agency_phone: str | None = None
    gtfs_agency_email: str | None = None
    
    def get_by_gtfs_id(gtfs_agency_id):
        query = f"SELECT * FROM agencies WHERE gtfs_agency_id LIKE '{gtfs_agency_id}'"
        db = Connection.get_cursor()
        db.execute(query)
        agency = db.fetchone()
        db.close()
        return agency
    
    def get_id_by_gtfs_id(gtfs_agency_id):
        agency = Agency.get_by_gtfs_id(gtfs_agency_id)
        if agency:
            return agency[0]
        return None
    
    def save(self):
        query = f"INSERT INTO agencies (name, gtfs_agency_id, gtfs_agency_url, gtfs_agency_timezone, gtfs_agency_lang, gtfs_agency_phone, gtfs_agency_email, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"
        db = Connection.get_cursor()
        db.execute(query, (self.name, self.gtfs_agency_id, self.gtfs_agency_url, self.gtfs_agency_timezone, self.gtfs_agency_lang, self.gtfs_agency_phone, self.gtfs_agency_email))
        db.connection.commit()
        db.close()
        
    def save_if_not_exists(self):
        agency = Agency.get_by_gtfs_id(self.gtfs_agency_id)
        if not agency:
            logger.info(f"Saving agency {self.name}")
            self.save()
        else:
            logger.info(f"Agency {self.name} already exists in the database")
    
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
        query = """
            INSERT INTO 
                stops (name, description, latitude, longitude, wheelchair_boarding, gtfs_stop_id, gtfs_stop_code, gtfs_location_type, gtfs_stop_timezone, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"""
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
    gtfs_agency_id: str | None = None # Esto no se guarda
    description: str | None = None
    route_type: int | None = None
    gtfs_route_id: str | None = None
    gtfs_route_short_name: str | None = None
    gtfs_route_long_name: str | None = None
    gtfs_route_url: str | None = None
    gtfs_route_color: str | None = None
    gtfs_route_text_color: str | None = None
    
    def get_by_gtfs_id(gtfs_route_id):
        query = f"SELECT * FROM lines WHERE gtfs_route_id LIKE '{gtfs_route_id}'"
        db = Connection.get_cursor()
        db.execute(query)
        line = db.fetchone()
        db.close()
        return line
    
    def save_and_upate_fk(self):
        query = f"""
        INSERT INTO lines (name, agency_id, description, route_type, gtfs_route_id, gtfs_route_short_name, gtfs_route_long_name, gtfs_route_url, gtfs_route_color, gtfs_route_text_color, created_at, updated_at) 
        VALUES (%s, (SELECT id FROM agencies WHERE gtfs_agency_id LIKE %s), %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"""
        db = Connection.get_cursor()
        db.execute(query, (self.name, self.gtfs_agency_id, self.description, self.route_type, self.gtfs_route_id, self.gtfs_route_short_name, self.gtfs_route_long_name, self.gtfs_route_url, self.gtfs_route_color, self.gtfs_route_text_color))
        db.connection.commit()
        db.close()
        
    def save_if_not_exists_and_update_fk(self):
        line = Line.get_by_gtfs_id(self.gtfs_route_id)
        if not line:
            logger.info(f"Saving line {self.name}")
            self.save_and_upate_fk()
        else:
            logger.info(f"Line {self.name} already exists in the database")
    
class Schedule(DbModel):
    table_name: str = "schedules"
    name: str
    gtfs_route_id: str 
    gtfs_service_id: str
    gtfs_trip_id: str
    gtfs_trip_short_name: str | None = None
    gtfs_bikes_allowed: int | None = None
    
    def get_by_gtfs_id(gtfs_trip_id):
        query = f"SELECT * FROM schedules WHERE gtfs_trip_id LIKE '{gtfs_trip_id}'"
        db = Connection.get_cursor()
        db.execute(query)
        schedule = db.fetchone()
        db.close()
        return schedule
    
    def save_and_update_fk(self):
        query = f"""
        INSERT INTO schedules (name, line_id, gtfs_service_id, gtfs_trip_id, gtfs_trip_short_name, gtfs_bikes_allowed, created_at, updated_at)
        VALUES (%s, (SELECT id FROM lines WHERE gtfs_route_id LIKE %s), %s, %s, %s, %s, NOW(), NOW())"""
        db = Connection.get_cursor()
        db.execute(query, (self.name, self.gtfs_route_id, self.gtfs_service_id, self.gtfs_trip_id, self.gtfs_trip_short_name, self.gtfs_bikes_allowed))
        db.connection.commit()
        db.close()
        
    def save_if_not_exists_and_update_fk(self):
        schedule = Schedule.get_by_gtfs_id(self.gtfs_trip_id)
        if not schedule:
            logger.info(f"Saving schedule {self.name} ({self.gtfs_trip_id})")
            self.save_and_update_fk()
        else:
            logger.info(f"Schedule {self.name} already exists in the database")
               
class ScheduleStop(DbModel):
    table_name: str = "schedule_stops"
    gtfs_stop_id: str
    arrival_time: str
    departure_time: str
    gtfs_trip_id: str
    shape_distance_traveled: float | None = None
    stop_sequence: int
    
    def get_by_gtfs_id(gtfs_trip_id, gtfs_stop_id, stop_sequence):
        query = f"SELECT * FROM schedule_stops WHERE stop_id = (SELECT id FROM stops WHERE gtfs_stop_id LIKE '{gtfs_stop_id}') AND schedule_id = (SELECT id FROM schedules WHERE gtfs_trip_id LIKE '{gtfs_trip_id}') AND stop_sequence = {stop_sequence}"
        db = Connection.get_cursor()
        db.execute(query)
        schedule_stop = db.fetchone()
        db.close()
        return schedule_stop
    
    def save_and_update_fk(self):
        
        for time in [self.arrival_time, self.departure_time]:
            if int(str(time).split(":")[0]) >= 24:
                time = time.replace(str(time).split(":")[0], str(int(str(time).split(":")[0]) - 24))
        
        arrival_time = datetime.strptime(self.arrival_time, "%H:%M:%S").time()
        departure_time = datetime.strptime(self.departure_time, "%H:%M:%S").time()
        
        query = f"""
        INSERT INTO schedule_stops (stop_id, arrival_time, departure_time, schedule_id, shape_distance_traveled, stop_sequence, created_at, updated_at)
        VALUES ((SELECT id FROM stops WHERE gtfs_stop_id LIKE %s), %s, %s, (SELECT id FROM schedules WHERE gtfs_trip_id LIKE %s), %s, %s, NOW(), NOW())"""
        db = Connection.get_cursor()
        db.execute(query, (self.gtfs_stop_id, arrival_time, departure_time, self.gtfs_trip_id, self.shape_distance_traveled, self.stop_sequence))
        db.connection.commit()
        db.close()
        
    def save_if_not_exists_and_update_fk(self):
        schedule_stop = ScheduleStop.get_by_gtfs_id(self.gtfs_trip_id, self.gtfs_stop_id, self.stop_sequence)
        if not schedule_stop:
            logger.info(f"Saving schedule stop {self.gtfs_stop_id} in schedule {self.gtfs_trip_id}")
            self.save_and_update_fk()
        else:
            logger.info(f"Schedule stop {self.gtfs_stop_id} in schedule {self.gtfs_trip_id} already exists in the database")