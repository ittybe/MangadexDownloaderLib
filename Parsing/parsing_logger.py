'''
init logger object for logging everything in this folder s modules 
'''
import logging 
import multiprocessing

parsing_logger = logging.getLogger(__name__)
multiprocess_parsing_logger = multiprocessing.get_logger()
