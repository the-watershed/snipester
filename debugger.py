import logging

def setup_debugging():
    """Set up the logging configuration."""
    logging.basicConfig(
        filename='debug.log',  # Log to a file named debug.log
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def debug(message, level='DEBUG'):

    """Log a debug message."""
    if level == 'DEBUG':
        logging.debug(message)
    elif level == 'INFO':
        logging.info(message)
    elif level == 'WARNING':
        logging.warning(message)
    elif level == 'ERROR':
        logging.error(message)
    elif level == 'CRITICAL':
        logging.critical(message)

    print(message)  # Also print to the console for immediate feedback
