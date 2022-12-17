from threading import Thread


def MyFunc(str,num):
    for i in range(num):
        print(f"{str} {i}")

thread1 = Thread(target=MyFunc, args=("Поток 1",10))
thread2 = Thread(target=MyFunc, args=("Поток 2",10))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
