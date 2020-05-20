import logging


class Logger:
    logger = logging.getLogger("logging_tryout2")
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter("%(asctime)s || %(levelname)s || %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
