import random
import time
from multiprocessing import Pool


def counter(_id, sleep_time):
    start = time.time()
    time.sleep(sleep_time)
    stop = time.time() - start
    print(f"{_id}: {stop}")


def main():
    with Pool(5) as p:
        map_list = []
        for i in range(10):
            sleep_time = random.randint(1, 5)
            map_list.append((i, sleep_time))
        p.starmap(counter, map_list)


if __name__ == '__main__':
    main()
