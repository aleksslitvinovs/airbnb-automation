import logging
import os
import threading
import time

import pytest

LOGGER = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--suite-timeout",
        action="store",
        type=int,
        default=None,
        help="Maximum time (in seconds) allowed for the entire test suite",
    )


def timeout_killer(timeout: int):
    time.sleep(timeout)
    LOGGER.error(f"\033[91mTest suite exceeded timeout of {timeout} seconds\033[0m")
    os._exit(1)


def pytest_sessionstart(session: pytest.Session):
    timeout = session.config.getoption("--suite-timeout")

    if timeout:
        thread = threading.Thread(target=timeout_killer, args=[timeout], daemon=True)
        thread.start()
