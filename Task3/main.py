from threading import Thread, Lock
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor


@dataclass
class Counter:
    value: int


def function(count, a):
    for _ in range(count):
        a.value += 1


def mutex_function(count, mtx, a):
    for _ in range(count):
        with mtx:
            a.value += 1


def main():
    mtx = Lock()
    a = Counter(0)
    with ThreadPoolExecutor(max_workers=5) as ex:
        for _ in range(5):
            ex.submit(function, 1000000, a)
    print("----------------------", a.value)
    a = Counter(0)
    with ThreadPoolExecutor(max_workers=5) as ex:
        for _ in range(5):
            ex.submit(mutex_function, 1000000, mtx, a)
    print("----------------------", a.value)


main()
