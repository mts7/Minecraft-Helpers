import os

import mtslogger
import pytest

import src.api.handler as handler


@pytest.mark.skipif(os.environ.get('CI'),
                    reason='GitHub Actions does not support arrays in config.')
def test_api_handler_init():
    logger = mtslogger.get_logger(__name__)
    log_level = 'debug'
    api = handler.ApiHandler(log_level)
    assert isinstance(api.logger, type(logger))
    assert api.logger.mode == log_level
