from pydantic import BaseModel

class GtfsAgency(BaseModel):
    """
    Agency.txt
    Una agencia de transporte público. Ejemplo: Renfe, EMT, etc.
    """
    agency_id: str
    agency_name: str
    agency_url: str
    agency_timezone: str
    agency_lang: str | None = None
    agency_phone: str | None = None
    agency_email: str | None = None
    
class GtfsStop(BaseModel):
    """
    Stops.txt
    Esta clase representa una parada de transporte público.
    """
    stop_id: str
    stop_code: str | None = None
    stop_name: str # Nombre de la parada
    stop_desc: str | None = None # Descripción de la parada
    stop_lat: float # Latitud
    stop_lon: float # Longitud
    
    """
    location_type indica el tipo de localización de la parada. Los valores posibles son:
    0 (or blank) - Stop (or Platform). A location where passengers board or disembark from a transit vehicle. Is called a platform when defined within a parent_station.
    1 - Station. A physical structure or area that contains one or more platform.
    2 - Entrance/Exit. A location where passengers can enter or exit a station from the street. If an entrance/exit belongs to multiple stations, it may be linked by pathways to both, but the data provider must pick one of them as parent.
    3 - Generic Node. A location within a station, not matching any other location_type, that may be used to link together pathways define in pathways.txt.
    4 - Boarding Area. A specific location on a platform, where passengers can board and/or alight vehicles.
    """
    location_type: int | None = None
    
    wheelchair_boarding: int = 0 # 0: No info, 1: Accesible, 2: No accesible
    stop_timezone: str | None = None # Zona horaria de la parada
    
class GtfsRoute(BaseModel):
    """
    Routes.txt
    Esta clase representa una linea GTFS. Una linea NO contiene información geografica
    Para nosotros es una Linea
    """
    route_id: str
    agency_id: str #! Este campo por lo general es opcional pero lo contaremos como obligatorio
    
    # Short name, long name debe haber OBIGATORIAMENTE uno de los dos que no sea None
    route_short_name: str | None = None # Nombre corto de la linea
    route_long_name: str | None = None
    
    route_desc: str | None = None # Descripción de la linea
    
    """
    route_type indica el tipo de transporte de la linea. Los valores posibles son:
    0 - Tram, Streetcar, Light rail. Any light rail or street level system within a metropolitan area.
    1 - Subway, Metro. Any underground rail system within a metropolitan area.
    2 - Rail. Used for intercity or long-distance travel.
    3 - Bus. Used for short- and long-distance bus routes.
    4 - Ferry. Used for short- and long-distance boat service.
    5 - Cable tram. Used for street-level rail cars where the cable runs beneath the vehicle (e.g., cable car in San Francisco).
    6 - Aerial lift, suspended cable car (e.g., gondola lift, aerial tramway). Cable transport where cabins, cars, gondolas or open chairs are suspended by means of one or more cables.
    7 - Funicular. Any rail system designed for steep inclines.
    11 - Trolleybus. Electric buses that draw power from overhead wires using poles.
    12 - Monorail. Railway in which the track consists of a single rail or a beam.
    """
    route_type: int
    route_url: str | None = None # URL de la linea
    route_color: str | None = None # Color de la linea
    route_text_color: str | None = None # Color del texto de la linea    
    
class GtfsTrip(BaseModel):
    """
    Trips.txt
    Esta clase representa un viaje de una linea GTFS. No contiene información geografica
    """
    route_id: str # Identificador de la linea
    service_id: str # ID del servicio, se corresponde con el ID de un Schedule en nuestra base de datos
    trip_id: str # ID del viaje, es único

    trip_headsign: str | None = None # Cabecera del viaje
    trip_short_name: str | None = None # Nombre corto del viaje
    shape_id: str | None = None # ID de la forma del viaje, se corresponde con el ID de shapes.txt
    
    bikes_allowed: int = 0 # 0: No info, 1: Permitido, 2: No permitido
    
class GtfsStopTime(BaseModel):
    """
    StopTimes.txt
    Esta clase representa un horario de una parada de una linea GTFS. No contiene información geografica.
    Se corresponde con un ScheduleStop en nuestra base de datos
    """
    trip_id: str # ID del viaje (Schedule) al que pertenece
    arrival_time: str # Hora de llegada
    departure_time: str # Hora de salida
    stop_id: str # ID de la parada
    stop_sequence: int # Orden de la parada en el viaje
    
    # Distancia recorrida en la forma del viaje, debe estar en la misma unidad que la forma
    shape_dist_traveled: float | None = None 
    
class GtfsCalendar(BaseModel):
    """
    OPCIONAL
    Calendar.txt
    Esta clase identifica los días en los que un servicio está disponible. (GTFSTrip)
    """
    service_id: str # ID del servicio
    monday: int # 0: No disponible, 1: Disponible
    tuesday: int # 0: No disponible, 1: Disponible
    wednesday: int # 0: No disponible, 1: Disponible
    thursday: int # 0: No disponible, 1: Disponible
    friday: int # 0: No disponible, 1: Disponible
    saturday: int # 0: No disponible, 1: Disponible
    sunday: int # 0: No disponible, 1: Disponible
    start_date: str # Fecha de inicio del servicio
    end_date: str # Fecha de fin del servicio
    
class GtfsCalendarDates(BaseModel):
    """
    OPCIONAL
    CalendarDates.txt
    Esta clase identifica excepciones a la disponibilidad de un servicio. (GTFSTrip)
    """
    service_id: str # ID del servicio
    date: str # Fecha de la excepción
    exception_type: int # 1: Servicio disponible, 2: Servicio no disponible
    
class GtfsShape(BaseModel):
    """
    OPCIONAL
    Shapes.txt
    Esta clase representa una forma de una linea GTFS. Contiene información geografica
    """
    shape_id: str # ID de la forma
    shape_pt_lat: float # Latitud
    shape_pt_lon: float # Longitud
    shape_pt_sequence: int # Orden de la parada en la forma
    shape_dist_traveled: float | None = None # Distancia recorrida en la forma
    