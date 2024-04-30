from pydantic import ValidationError
from models.gtfs import GtfsStop, GtfsAgency, GtfsRoute
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
                    agency_phone=str(int(row['agency_phone'])) if not pd.isna(row['agency_phone']) else None,
                    agency_email=row['agency_email'] if not pd.isna(row['agency_email']) else None
                )
                parsed_agencies.append(agency)
            except ValidationError as exc:
                logger.error(f'Error parsing agency {row["agency_id"]}: {exc}')
                
        agencies_db = []
        for agency in parsed_agencies:
            agencies_db.append(agency.getDbModel())
            
        return agencies_db