import logging
import sys
import socket
from datetime import datetime as dt
import traceback

host = socket.gethostname()

def setup_logging(loglevel, logfile):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if numeric_level is None:
        raise ValueError("Invalid log level: %s" % loglevel)

    log_format = "[%(asctime)s] {0}/%(levelname)s/%(name)s: %(message)s".format(host)
    logging.basicConfig(level=numeric_level, filename=logfile, format=log_format)

    sys.stderr = StdErrWrapper()
    sys.stdout = StdOutWrapper()

stdout_logger = logging.getLogger("stdout")
stderr_logger = logging.getLogger("stderr")

class StdOutWrapper(object):
    """
    Wrapper for stdout
    """
    def write(self, s):
        if s == None or s.strip() == '':
            return
        stdout_logger.info(s.strip())

class StdErrWrapper(object):
    """
    Wrapper for stderr
    """
    def write(self, s):
        if s == None or s.strip() == '':
            return
        stderr_logger.error(s.strip())

# set up logger for the statistics tables
console_logger = logging.getLogger("console_logger")
# create console handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
# formatter that doesn't include anything but the message
sh.setFormatter(logging.Formatter('%(message)s'))
console_logger.addHandler(sh)
console_logger.propagate = False

# configure python-requests log level
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

_csv_log_file = None
_csv_logger = None
def setup_csv_logging(log_file_path, custom_event_keys):
    import events
    import csv
    global _csv_logger, _csv_log_file
    fields = ["timestamp", "request_type", "name", "response_time", "response_length", "exception"]
    if custom_event_keys:
        fields = fields + custom_event_keys
    _csv_log_file = open(log_file_path, 'w', buffering=1) # Line buffered.
    _csv_logger = csv.DictWriter(_csv_log_file, fieldnames=fields, extrasaction='ignore')
    _csv_logger.writeheader()
    events.request_success += log_to_csv
    events.request_failure += log_to_csv
    events.locust_error += log_to_csv
        
def log_to_csv(**kwargs):
    kwargs.setdefault('timestamp', dt.isoformat(dt.utcnow()))
    if 'tb' in _csv_logger.fieldnames and 'tb' in kwargs:
        kwargs['tb'] = traceback.extract_tb(kwargs['tb'])[-1]
    _csv_logger.writerow(kwargs)
