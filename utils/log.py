import logging

class Logger:
    __instance = None
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        self.logger = logger
        
    @staticmethod
    def get_logger():
        if Logger.__instance is None:
            Logger.__instance = Logger()
            
        return Logger.__instance.logger
        
        