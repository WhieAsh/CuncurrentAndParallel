import os
import threading

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from multiprocessing import Queue
from queue import Empty


class PostgresMasterScheduler(threading.Thread):
    def __init__(self, input_queue: Queue, **kwargs):
        if 'out_queues' in kwargs:
            kwargs.pop('out_queues')
        super(PostgresMasterScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue

        self.start()

    def run(self) -> None:
        while True:
            try:
                value = self._input_queue.get(timeout=10)
            except Empty:
                print('Timeout reached in PG scheduler stopping...')
                break
            if value == 'DONE':
                break
            symbol, price, _extract_dttm = value
            postgres_worker = PostgresWorker(symbol, price, _extract_dttm)
            postgres_worker.insert_into_db()


class PostgresWorker():
    def __init__(self, symbol, price, extract_dttm):
        self._symbol = symbol
        self._price = price
        self._extract_dttm = extract_dttm

        self._PG_HOST = os.environ.get('PG_HOST') or 'localhost'
        self._PG_DATABASE = os.environ.get('PG_DATABASE') or 'postgres'
        self._PG_USER = os.environ.get('PG_USER') or 'postgres'
        self._PG_PASSWORD = os.environ.get('PG_PASSWORD') or 'postgres'

        self._engin = create_engine(f'postgresql://{self._PG_USER}:{self._PG_PASSWORD}@{self._PG_HOST}:5432/{self._PG_DATABASE}')

    def _get_insert_stetment(self):

        sql_stm = """INSERT INTO prices (symbol, price, extract_dttm) values(:symbol, :price, :extract_dttm)"""

        return sql_stm

    def insert_into_db(self):
        insert_stm = self._get_insert_stetment()

        with self._engin.connect() as conn:
            conn.execute(text(insert_stm), {'symbol':self._symbol,
                                            'price': self._price,
                                            'extract_dttm': str(self._extract_dttm)})
            conn.commit()
