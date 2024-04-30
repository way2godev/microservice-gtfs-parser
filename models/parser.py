from pydantic import ValidationError
from models.gtfs import GtfsStop, GtfsAgency, GtfsRoute, GtfsTrip, GtfsStopTime
import pandas as pd

class DataParser:
    
    @staticmethod
    def stops(stops_dataframe, logger):
        parsed_stops = []

        for i, row in stops_dataframe.iterrows():
            try:
                stop = GtfsStop(
                stop_id=row['stop_id'],
                stop_code=str(row['stop_code']),
                stop_name=row['stop_name'],
                stop_desc=row['stop_desc'] if not pd.isna(row['stop_desc']) else None,
                stop_lat=float(row['stop_lat']),
                stop_lon=float(row['stop_lon']),
                location_type=row['location_type'],
                stop_timezone=row['stop_timezone'] if not pd.isna(row['stop_timezone']) else None,
                wheelchair_boarding=row['wheelchair_boarding'] if not pd.isna(row['wheelchair_boarding']) else 0
                )
                parsed_stops.append(stop)
            except ValidationError as exc:
                logger.error(f'Error parsing stop {row["stop_id"]}: {exc}')
            
        stops_db = []
        for stop in parsed_stops:
            stops_db.append(stop.getDbModel())
            
        return stops_db
    
    @staticmethod
    def routes(routes_dataframe, logger):
        parsed_routes = []
        
        for i, row in routes_dataframe.iterrows():
            try:
                route = GtfsRoute(
                    route_id=row['route_id'],
                    agency_id=row['agency_id'],
                    route_short_name=row['route_short_name'],
                    route_long_name=row['route_long_name'],
                    route_desc=row['route_desc'] if not pd.isna(row['route_desc']) else None,
                    route_type=row['route_type'],
                    route_url=row['route_url'] if not pd.isna(row['route_url']) else None,
                    route_color=row['route_color'] if not pd.isna(row['route_color']) else None,
                    route_text_color=row['route_text_color'] if not pd.isna(row['route_text_color']) else None
                )
                parsed_routes.append(route)
            except ValidationError as exc:
                logger.error(f'Error parsing route {row["route_id"]}: {exc}')
                
        routes_db = []
        
        for route in parsed_routes:
            routes_db.append(route.getDbModel())
            
        return routes_db
    
    @staticmethod
    def schedules(routes_dataframe, logger):
        parsed_schedules = []
        
        for i, row in routes_dataframe.iterrows():
            try:
                schedule = GtfsTrip(
                    route_id=row['route_id'],
                    service_id=row['service_id'],
                    trip_id=row['trip_id'],
                    trip_headsign=row['trip_headsign'] if not pd.isna(row['trip_headsign']) else None,
                    shape_id=row['shape_id'] if not pd.isna(row['shape_id']) else None,
                    bikes_allowed=row['bikes_allowed'] if not pd.isna(row['bikes_allowed']) else 0
                )
                parsed_schedules.append(schedule)
            except ValidationError as exc:
                logger.error(f'Error parsing schedule {row["trip_id"]}: {exc}')
                
        schedules_db = []
        
        for schedule in parsed_schedules:
            schedules_db.append(schedule.getDbModel())
            
        return schedules_db
    
    @staticmethod
    def agencies(agencies_dataframe, logger):
        parsed_agencies = []
        
        for i, row in agencies_dataframe.iterrows():
            try:
                agency = GtfsAgency(
                    agency_id=row['agency_id'],
                    agency_name=row['agency_name'],
                    agency_url=row['agency_url'],
                    agency_timezone=row['agency_timezone'],
                    agency_lang=row['agency_lang'] if not pd.isna(row['agency_lang']) else None,
                    agency_phone=str(row['agency_phone']) if not pd.isna(row['agency_phone']) else None,
                    agency_email=row['agency_email'] if not pd.isna(row['agency_email']) else None
                )
                parsed_agencies.append(agency)
            except ValidationError as exc:
                logger.error(f'Error parsing agency {row["agency_id"]}: {exc}')
                
        agencies_db = []
        for agency in parsed_agencies:
            agencies_db.append(agency.getDbModel())
            
        return agencies_db
    
    @staticmethod
    def stop_times(stop_times_dataframe, logger):
        parsed_stop_times = []
        
        for i, row in stop_times_dataframe.iterrows():
            try:
                stop_time = GtfsStopTime(
                    trip_id=row['trip_id'],
                    arrival_time=row['arrival_time'],
                    departure_time=row['departure_time'],
                    stop_id=row['stop_id'],
                    stop_sequence=row['stop_sequence'],
                    shape_dist_traveled=row['shape_dist_traveled'] if not pd.isna(row['shape_dist_traveled']) else None
                )
                parsed_stop_times.append(stop_time)
            except ValidationError as exc:
                logger.error(f'Error parsing stop time {row["trip_id"]}: {exc}')
                
        stop_times_db = []
        
        for stop_time in parsed_stop_times:
            stop_times_db.append(stop_time.getDbModel())
            
        return stop_times_db