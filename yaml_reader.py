import threading
import time

from multiprocessing import Queue
import importlib

import yaml

class YamlPiplineExecutor(threading.Thread):

    def __init__(self, pipline_file):
        super(YamlPiplineExecutor, self).__init__()
        self._pipline_file = pipline_file
        self._queues = {}
        self._workers = {}
        self._workers_threads = {}
        self._queue_reader_count = {}
        self._worker_out_queue = {}

    def _init_pipline(self):
        with open(self._pipline_file, 'r') as inFile:
            self.pipline_document = yaml.safe_load(inFile)

    def _init_queues(self):
        for queue in self.pipline_document['queues']:
            queue_name = queue['name']
            self._queues[queue_name] = Queue()

    def _init_workers(self):
        for worker in self.pipline_document['workers']:
            worker_class = getattr(importlib.import_module(worker['class_path']), worker['class'])

            worker_name = worker['name']
            instances_number = worker.get('instances', 1)

            class_parameters = {}

            if 'input_queue' in worker:
                input_queue = self._queues[worker['input_queue']]
                class_parameters['input_queue'] = input_queue
                self._queue_reader_count[worker['input_queue']] = instances_number

            if 'out_queues' in worker:
                out_queue = self._queues[worker['out_queues'][0]]
                class_parameters['out_queues'] = [out_queue]
                self._worker_out_queue[worker_name] = worker['out_queues'][0]

            if 'inout_values' in worker:
                inout_value = worker['inout_values'][0]
                class_parameters['inout_value'] = inout_value

            worker_list = []
            for instance in range(instances_number):
                worker_instance = worker_class(**class_parameters)

                worker_list.append(worker_instance)

            self._workers[worker_name] = worker_list

    def _join_workers(self):
        for worker_name in self._workers:
            for worker_thread in self._workers[worker_name]:
                worker_thread.join()

    def process_pipline(self):
        self._init_pipline()
        self._init_queues()
        self._init_workers()
        #self._join_workers()


    def run(self) -> None:
        self.process_pipline()

        total_active_threads = -1
        while total_active_threads != 0:
            total_active_threads = 0
            active_workers = {}
            dead_workers = []
            for worker in self._workers:
                aliver_threads_count = 0
                for worker_thread in self._workers[worker]:
                    if worker_thread.is_alive():
                        aliver_threads_count += 1
                        total_active_threads += 1
                active_workers[worker] = aliver_threads_count
                if aliver_threads_count == 0:
                    dead_workers.append(worker)

            print(f"active_workers: {active_workers}")

            active_queues = {}
            for queue in self._queues:
                active_queues[queue] = self._queues[queue].qsize()

            print(f"Queue size: {active_queues}")

            for worker in dead_workers:
                if worker in self._worker_out_queue:
                    out_queue = self._worker_out_queue[worker]
                    reader_count = self._queue_reader_count[out_queue]
                    for i in range(reader_count):
                         self._queues[out_queue].put('DONE')
                self._workers.pop(worker)
            time.sleep(1)
