import os
import pandas as pd
from models.parser import DataParser
from db.connection import Connection
import dotenv
from utils.log import Logger
from concurrent.futures import ThreadPoolExecutor

FILES_MANDATORY = ['agency', 'routes', 'stops', 'trips', 'stop_times']
FILES_ALL = ['agency', 'calendar', 'calendar_dates', 'fare_attributes', 'fare_rules', 'feed_info', 'frequencies', 'routes', 'shapes', 'stop_times', 'stops', 'transfers', 'trips']
MAX_WORKERS = 5

logger = Logger.get_logger()

dotenv.load_dotenv()

if not all([os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD')]):
    logger.error('Missing environment variables')
    logger.error('Please make sure you have the following environment variables set:')
    logger.error('DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD')
    logger.error('Actual values: ', os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))
    exit(1)

Connection(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
).connect(logger=logger)

def download_data_compressed(url):
    """
    Función que descarga los ficheros GTFS y los descomprime
    """
    logger.info(f'Downloading {url}')
    os.system(f'curl -o ./data/gtfs.zip {url}')
    os.system(f'unzip ./data/gtfs.zip -d ./data/')
    os.remove(f'./data/gtfs.zip')
    logger.info('Downloaded and extracted GTFS data')

def parse_source_to_db():
    """
    Función que parsea los ficheros GTFS a la base de datos
    """
    logger.info('Parsing downloaded GTFS data')
    for file in FILES_MANDATORY:
        if not os.path.exists(f'./data/{file}.csv'):
            if os.path.exists(f'./data/{file}.txt'):
                os.rename(f'./data/{file}.txt', f'./data/{file}.csv')
            else:
                logger.error(f'File {file}.csv not found in data/ directory')
                return
            
    agencies_raw = pd.read_csv('./data/agency.csv')
    parsed_agencies = DataParser.agencies(agencies_raw, logger)
    logger.info(f'Found {len(parsed_agencies)} agencies')
    for agency in parsed_agencies:
        agency.save_if_not_exists()
    logger.info(f'Parsed {len(parsed_agencies)} agencies')
    
    routes_raw = pd.read_csv('./data/routes.csv')
    logger.info(f'Found {len(routes_raw)} routes')
    parsed_routes = DataParser.routes(routes_raw, logger)
    for route in parsed_routes:
        route.save_if_not_exists_and_update_fk()
    
    schedules_raw = pd.read_csv('./data/trips.csv')
    logger.info(f'Found {len(schedules_raw)} schedules')
    parsed_schedules = DataParser.schedules(schedules_raw, logger)
    for schedule in parsed_schedules:
        schedule.save_if_not_exists_and_update_fk()
    logger.info(f'Parsed {len(parsed_schedules)} schedules')
    
    stops_raw = pd.read_csv('./data/stops.csv')
    logger.info(f'Found {len(stops_raw)} stops')
    parsed_stops = DataParser.stops(stops_raw, logger)
    for stop in parsed_stops:
        stop.save_if_not_exists()
    logger.info(f'Parsed {len(parsed_stops)} stops')

def cleanup_data():
    """
    Función que limpia los ficheros GTFS
    """
    logger.info('Cleaning up data')
    for file in FILES_ALL:
        if os.path.exists(f'./data/{file}.csv'):
            os.remove(f'./data/{file}.csv')
        if os.path.exists(f'./data/{file}.txt'):
            os.remove(f'./data/{file}.txt')
    logger.info('Data cleaned up')
    
    
if __name__ == '__main__':
    sources = pd.read_csv('./sources.csv')
    logger.info(f'Found {len(sources)} GTFS data sources')
    
    if not os.path.exists('./data'):
        os.mkdir('./data')
    else:   
        for file in os.listdir('./data'):
            os.remove(f'./data/{file}')
    
    for i, row in sources.iterrows():
        logger.info(f'Processing source {row["Feed Name"]} ({row["Provider"]} - {row["Location"]})  ({i+1}/{len(sources)})')
        download_data_compressed(row['download_url'])
        parse_source_to_db() 
        cleanup_data()
        
    
    