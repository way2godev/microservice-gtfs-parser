from pydantic import ValidationError
from models.gtfs import GtfsStop
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