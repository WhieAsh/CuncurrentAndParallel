import threading


class SumSqquareWorker(threading.Thread):
    def __init__(self, n, **kwargs):
        super(SumSqquareWorker, self).__init__(**kwargs)
        self._n = n
        self.start()

    def calc_sum_of_squares(self):
        sum_of_squrrs = 0
        iteration = (self._n+1) * 10000000
        #print(iteration)
        for i in range(iteration):
            sum_of_squrrs +=  i * 2
        print(sum_of_squrrs)

    def run(self):
        self.calc_sum_of_squares()
