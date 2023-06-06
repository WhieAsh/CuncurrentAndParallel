from multiprocessing import Queue
import importlib

import yaml

class YamlReader():
    def __int__(self, pipline_file):
        self._pipline_file = pipline_file
        self._queues = {}
        self.workers = {}


    def _init_pipline(self):
        with open(self._pipline_file, 'r') as inFile:
            self.pipline_document = yaml.safe_load(inFile)

    def _init_queues(set):
        for queue in self.pipline_document['queues']:
            queue_name = queue.['name']
            self._queues[queue_name] = Queue()

    def _init_workers(self):
        for worker in self.pipline_document['qorkers']:
            worker_class = getatr(importlib.import_module(worker['class_path']), worker['class'])

            worker_name = worker['name']
            worker_list = []
            for instance in range(worker['instances']):
                worker_instance = worker_class(input_queue=self._queues['WikiSymbols'], \
                                                out_queues=[self._queues['PostgresTasks'])
                worker_list.append(worker_instance)

            self._workers[worker_name] = worker_list

    def _join_workers():
        for worker_name in self._workers:
            for worker_thread in self._workers[worker_name]:
                worker_thread.join()


    def process_pipline(self):
        self._init_pipline()
        self._init_queues()
        self._init_workers()
        self._join_workers()


