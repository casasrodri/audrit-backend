import sys
from loguru import logger
from config.env import Logger

format_time = "<cyan>{time:HH:mm:ss}</cyan>"
format_level = "<level>{level}</level>"
format_file_line = " <i><le>{file}:{line}</le></i>" if Logger.FILE_LINE else ""
format_message = "{message}"
logger.remove(0)

logger.add(
    sys.stdout,
    format=f"{format_time} {format_level}{format_file_line} <b>→</b> {format_message}",
    colorize=True,
    level=Logger.LEVEL,
)

logger.level("WHO?", no=5, color="<green>")
logger.who = lambda msg: logger.log("WHO?", msg)

logger.level("CAN?", no=5, color="<yellow>")
logger.can = lambda msg: logger.log("CAN?", msg)

# logger.trace("A trace message.")
# logger.debug("A debug message.")
# logger.info("An info message.")
# logger.success("A success message.")
# logger.warning("A warning message.")
# logger.error("An error message.")
# logger.critical("A critical message.")

# logger.who("Se está logueando Rodri")
# logger.can("Permiso concedido :D")
