import sys
import time
import multiprocessing

STDOUT_PATH = 'attempt1.txt'

def wrap(task, path):
    def wrapper(*args, **kwargs):
        # with open(os.path.join(path, name), 'x') as f:
        with open(path, 'x') as f:
            sys.stdout = f
            sys.stderr = f
            task(*args, **kwargs)
    return wrapper

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print('Lorem ipsumer')


def run():
    eprint("Lorem ipsum")
if __name__ == '__main__':
    process_handler = multiprocessing.Process(target=wrap(run, STDOUT_PATH), daemon=True)
    process_handler.start()
    time.sleep(1)
    process_handler.join()