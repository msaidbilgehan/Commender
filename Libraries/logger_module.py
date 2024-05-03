import logging
import sys
from paths import root_path_logs



# Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger_stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
logger_file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

logger_stdout_handler = logging.StreamHandler(sys.stdout)
logger_stdout_handler.setLevel(logging.DEBUG)
logger_stdout_handler.setFormatter(logger_stdout_formatter)

logger_file_handler = logging.FileHandler(root_path_logs)
logger_file_handler.setLevel(logging.DEBUG)
logger_file_handler.setFormatter(logger_file_formatter)

logger.addHandler(logger_file_handler)
logger.addHandler(logger_stdout_handler)



# Global Logger
# global_logger = logging.getLogger("Global Logger")
# global_logger.setLevel(logging.INFO)

# global_logger_stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
# global_logger_file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

# global_logger_stdout_handler = logging.StreamHandler(sys.stdout)
# global_logger_stdout_handler.setLevel(logging.DEBUG)
# global_logger_stdout_handler.setFormatter(global_logger_stdout_formatter)

# global_logger_file_handler = logging.FileHandler(root_path_global_logs)
# global_logger_file_handler.setLevel(logging.DEBUG)
# global_logger_file_handler.setFormatter(global_logger_file_formatter)

# global_logger.addHandler(global_logger_file_handler)
# global_logger.addHandler(global_logger_stdout_handler)
