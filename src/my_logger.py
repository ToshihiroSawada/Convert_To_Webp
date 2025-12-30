"""logging."""

import logging

import settings


def my_logger(name: str) -> logging.Logger:
    """Create logging formats."""
    _st = settings
    log_level = getattr(logging, _st.LOG_LEVEL)
    filename = "./Result.log"
    logging.basicConfig(
        level=log_level,
        filename=filename,
        format="%(asctime)s, %(levelname)s, %(message)s, %(lineno)d",
        force=True,
    )
    return logging.getLogger(name)


def shutdown() -> None:
    """loggingの終了処理."""
    log = logging
    # loggingの終了処理を明示的に行う
    log.shutdown()
