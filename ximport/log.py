import sys
import logging


def get_logger(logger_name):
    root = logging.getLogger(logger_name)
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d [%(processName)s] [%(threadName)s] [%(filename)s] [%(module)s] [%(lineno)-5.5d] [%(levelname)-1.1s]  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root


if __name__ == "__main__":
    log = get_logger(__name__)
    log.info("test")
