from multiprocessing import Queue
from workers.PostgresWorker import PostgresMasterScheduler


out_queue = Queue()

pg_m = PostgresMasterScheduler(out_queue)

out_queue.put('DONE')