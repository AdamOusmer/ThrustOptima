import logging


def init_logger(trace: bool = False) -> logging.Logger:

    log_level = logging.DEBUG if trace else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="[ %(name)s ] - < %(levelname)s > : %(message)s",
    )


