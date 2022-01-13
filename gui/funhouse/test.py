import multiprocessing
import logging
from logging.handlers import QueueHandler, QueueListener
import time
import random


def f(i):
    time.sleep(random.uniform(.01, .05))
    logging.info('function called with {} in worker thread.'.format(i))
    time.sleep(random.uniform(.01, .05))
    return i


def worker_init(q):
    # all records from worker processes go to qh and then into q
    qh = QueueHandler(q)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(qh)


def logger_init():
    q = multiprocessing.Queue()
    # this is the handler for all log records
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(asctime)s - %(process)s - %(message)s"))

    # ql gets records from the queue and sends them to the handler
    ql = QueueListener(q, handler)
    ql.start()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # add the handler to the logger so records from this process are handled
    logger.addHandler(handler)

    return ql, q


def main():
    q_listener, q = logger_init()

    logging.info('hello from main thread')
    pool = multiprocessing.Pool(4, worker_init, [q])
    for result in pool.map(f, range(10)):
        pass
    pool.close()
    pool.join()
    q_listener.stop()

if __name__ == '__main__':
    main()