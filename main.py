import time
import threading

from workers.SumSquareWorkers import SumSqquareWorker
from workers.SpeepWorkers import SleppWorker

def main():
    current_time = time.time()
    my_workers = []
    for i in range(5):
        sum_sqquare_worker = SumSqquareWorker(i)
        my_workers.append(sum_sqquare_worker)

    for i in range(len(my_workers)):
        my_workers[i].join()
    print("Execution_time: ", round((time.time() - current_time)/1, 2))

    current_time = time.time()
    my_workers = []

    for i in range(5):
        slepp_worker = SleppWorker(i+1)
        my_workers.append(slepp_worker)

    for i in range(len(my_workers)):
        my_workers[i].join()
    print("Execution_time: ", round((time.time() - current_time)/1, 2))


if __name__ == "__main__":
    main()
