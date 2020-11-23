from threading import Thread, Lock


a = 0
mtx = Lock()


def function(arg):
    global a
    for _ in range(arg):
        a += 1


def mutex_function(arg):
    global a
    for _ in range(arg):
        with mtx:
            a += 1


def main():
    global a
    threads = []
    for _ in range(5):
        thread = Thread(target=function, args=(1000000,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    print("----------------------", a)
    a = 0
    for _ in range(5):
        thread = Thread(target=mutex_function, args=(1000000,))
        thread.start()
        threads.append(thread)
    [t.join() for t in threads]
    print("----------------------", a)


main()
