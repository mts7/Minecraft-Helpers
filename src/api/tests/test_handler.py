import mtslogger

import src.api.handler as handler


def test_api_handler_init():
    logger = mtslogger.get_logger(__name__)
    log_level = 'debug'
    api = handler.ApiHandler(log_level)
    assert isinstance(api.logger, type(logger))
    assert api.logger.mode == log_level
