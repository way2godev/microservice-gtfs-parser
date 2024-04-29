import os
import pandas as pd
from models.parser import DataParser
from db.connection import Connection
import dotenv
from utils.log import Logger
from concurrent.futures import ThreadPoolExecutor

FILES_MANDATORY = ['agency', 'routes', 'stops', 'trips', 'stop_times']
FILES_ALL = ['agency', 'calendar', 'calendar_dates', 'fare_attributes', 'fare_rules', 'feed_info', 'frequencies', 'routes', 'shapes', 'stop_times', 'stops', 'transfers', 'trips']
total_stop_count = 0

logger = Logger.get_logger()

dotenv.load_dotenv()

if not all([os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD')]):
    logger.error('Missing environment variables')
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

    stops_raw = pd.read_csv('./data/stops.csv')
    parsed_stops = DataParser.stops(stops_raw, logger)
    
    def save_stop(stop):
        stop.save_if_not_exists()

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(save_stop, parsed_stops)

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
        
    logger.info(f'Parsed {total_stop_count} stops in total')
    
    