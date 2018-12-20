import logging
import base64
from structlog import wrap_logger


logger = wrap_logger(logging.getLogger(__name__))


def log_api_error(status: int, error_msg: str, query: str):
    """ Depending on the severity of the response, log at an appropriate level """
    if status in [400, 401, 404]:
        logger.info(error_msg, status=status, query=query)
    elif status == 500:
        logger.error(error_msg, status=status, query=query)


def base_64_encode(to_encode: str) -> str:
    """ Encode a string using base64, for Basic Authentication """
    return base64.b64encode(to_encode.encode())
