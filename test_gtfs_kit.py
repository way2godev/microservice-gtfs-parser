import gtfs_kit as gk
import os
import geopandas as gp
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

path = "data/improved-gtfs-alsa-autobuses.zip"
print(gk.list_feed(path))


feed = gk.read_feed(path, dist_units='km')
stops = feed.get_stops()
print(stops.head())

routes = feed.get_routes()
print(routes.head())

week = feed.get_first_week()
week = feed.get_week(4)
feed.build_route_timetable(route_id='1576-8120011200VRE', dates=week).to_csv("data/route_timetable.csv")
gk.build_stop_timetable(feed, stop_id='1576-81200', dates=week).to_csv("data/stop_timetable.csv")
print(feed.describe())

trip_stats = feed.compute_trip_stats()
dates = [week[4], week[6]]
fts = feed.compute_feed_time_series(trip_stats, dates, freq='6h')


trip_stats = feed.compute_trip_stats()
print(trip_stats)

trip_stats.to_csv("data/trip_stats.csv")

gk.downsample(fts, freq='1h').to_csv("data/feed_time_series.csv")

feed_stats = feed.compute_feed_stats(trip_stats, week)
feed_stats.to_csv("data/feed_stats.csv")

rts = feed.compute_route_time_series(trip_stats, dates, freq='12h')
rts.to_csv("data/route_time_series.csv")