import os
from models import Agency, Line
import polars as pl

FOLDER = "google_zip"

FILES = ["agency.csv", "calendar.csv", "calendar_dates.csv", "routes.csv", "stops.csv", "trips.csv"]

def parse_agency(agency_df: pl.DataFrame):
    agencies = []
    for row in agency_df.iter_rows():
        row = dict(zip(agency_df.columns, row))
        agencies.append(Agency(
            id=row['agency_id'],
            name=row['agency_name'],
            raw_id=row['agency_id'],
            url=row['agency_url'],
            phone_number=row['agency_phone']
        ))

    return agencies

agency_df = pl.read_csv(os.path.join(FOLDER, "agency.csv"))
calendar_df = pl.read_csv(os.path.join(FOLDER, "calendar.csv"))
calendar_dates_df = pl.read_csv(os.path.join(FOLDER, "calendar_dates.csv"),)
routes_df = pl.read_csv(os.path.join(FOLDER, "routes.csv"))
stops_df = pl.read_csv(os.path.join(FOLDER, "stops.csv"))
stations_df = pl.read_excel("listado-estaciones-completo.xlsx", infer_schema_length=10000)
trips_df = pl.read_csv(os.path.join(FOLDER, "trips.csv"))

for col in agency_df.columns:
    agency_df = agency_df.rename({col: col.strip()})

for col in routes_df.columns:
    routes_df = routes_df.rename({col: col.strip()})

for col in stops_df.columns:
    stops_df = stops_df.rename({col: col.strip().lower()})

for col in stations_df.columns:
    stations_df = stations_df.rename({col: col.strip().lower()})

agencies = parse_agency(agency_df)

lines = []
for row in routes_df.iter_rows():
    row = dict(zip(routes_df.columns, row))
    lines.append(Line(
        id=row['route_id'],
        name=row['route_short_name'],
        agency=next(filter(lambda x: x.id == row['agency_id'], agencies), None),
    ))


stops_df = stops_df.join(stations_df, left_on='stop_id', right_on='código')

print(stops_df.columns)

for row in stops_df.iter_rows():
    ...