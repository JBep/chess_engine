
import logging
import time
import functools


def setup_log(level):
    logging.basicConfig(
        level=level,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),  # Log to a file
            #logging.StreamHandler()  # Log to the console
        ]
    )
    
def log_execution_time(func):
    """Decorator that logs the time a function takes to execute."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)
        end_time = time.time()    # Record the end time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        logging.log(level= logging.DEBUG, msg = f"Function '{func.__name__}' executed in {elapsed_time:.6f} seconds")
        return result
    return wrapper