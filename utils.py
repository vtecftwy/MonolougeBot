import logging
import os
import sys
from datetime import datetime
from functools import wraps
from pathlib import Path

# TODO: correct this line after transforming this into a package
ROOT = Path(__file__).parent
sys.path.append(str(ROOT.absolute()))

def logthis(*args):
    text = ' '.join([str(element) for element in args])
    logging.info(text)

def monitor_fn(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        logthis(f"Entering `{fn.__name__}`")
        res = fn(*args, **kwargs)
        logthis(f"Exiting  `{fn.__name__}`")
        return res
    return wrapper

def setup_logging():
    p2log = ROOT / 'logs/_anna.log'
    print(f"Logging into {p2log.absolute()}.")
    os.makedirs(p2log.parent, exist_ok=True)
    if not p2log.exists(): p2log.touch()

    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG) #Set the root logger to catpure all levels of logs

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Create a file handler to log to a file
    file_handler = logging.FileHandler(filename=p2log, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Set the log level for the file handler
    file_handler.setFormatter(formatter)

    # Create a stream handler for console output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)  # Set the log level for the console handler
    console_handler.setFormatter(formatter)

    # Add both handlers to the root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    print('Logging setup done')

    # # Configure the root logger
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='%(asctime)s %(message)s',
    #     datefmt='%H:%M:%S'
    #     )
    # # Create a file handler to log to a file
    # file_handler = logging.FileHandler(
    #     filename=p2log,
    #     mode='a',   
    #     encoding='utf-8'
    #     )
    # file_handler.setLevel(logging.DEBUG)  # Set the log level for the file handler
    # file_handler.setFormatter(
    #     fmt=logging.Formatter(
    #         fmt='%(asctime)s %(message)s',
    #         datefmt='%Y-%m-%d %H:%M:%S'
    #         )    
    #     )
    # # Add the file handler to the root logger
    # logging.getLogger('').addHandler(file_handler)
    