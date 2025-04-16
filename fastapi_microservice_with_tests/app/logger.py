import logging


def setup_logging(request_id):
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Request ID: {request_id} - Logging Started")
