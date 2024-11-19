
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

# Dictionary to keep track of function call statistics
function_stats = {}

def log_execution(func):
    """A decorator to log function execution details, including total and average time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Start timing the function execution
        start_time = time.time()

        # Execute the function
        result = func(*args, **kwargs)

        # Calculate execution time
        elapsed_time = time.time() - start_time
        function_name = func.__name__

        # Update statistics for the function
        if function_name not in function_stats:
            function_stats[function_name] = {
                "count": 0,
                "total_time": 0.0,
            }
        function_stats[function_name]["count"] += 1
        function_stats[function_name]["total_time"] += elapsed_time
        average_time = function_stats[function_name]["total_time"] / function_stats[function_name]["count"]

        # Log the function call details
        logging.info(
            f"Function '{function_name}' called {function_stats[function_name]['count']} time(s). "
            f"Total time: {function_stats[function_name]['total_time']:.4f} seconds. "
            f"Average time: {average_time:.4f} seconds."
        )

        return result
    return wrapper

def print_function_stats():
    print("Function calls:\n---------------------------------------------")

    for function, stats in sorted(function_stats.items(), key = lambda item: item[1]["total_time"]):
        average_time = stats["total_time"] / stats["count"]
        print(f"Function {function} called {stats["count"]} times, total runtime: {stats['total_time']:.4f} second, average {average_time:.4f} seconds."
              )
        