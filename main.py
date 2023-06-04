import time
import threading
from multiprocessing import Queue

from workers.WikiWorker import WikiWorker
from workers.YahooFinancePriceWorker import YahooFinanceScheduler
from workers.PostgresWorker import PostgresMasterScheduler


def main():
    symbol_queue = Queue()
    out_queue = Queue()
    current_time = time.time()
    wiki_worker = WikiWorker()

    yahoo_finance_scheduler_num = 1
    yahoo_finance_scheduler_count = []
    for i in range(yahoo_finance_scheduler_num):
        yahoo_finance_scheduler = YahooFinanceScheduler(symbol_queue, [out_queue])
        yahoo_finance_scheduler_count.append(yahoo_finance_scheduler)

    pg_scheduler_num = 2
    pg_scheduler_count = []
    for i in range(pg_scheduler_num):
        postgres_master_scheduler = PostgresMasterScheduler(out_queue)
        pg_scheduler_count.append(postgres_master_scheduler)

    sybol_count = 0
    for symbol in wiki_worker.get_500_companies():
        symbol_queue.put(symbol)
        sybol_count += 1
        print(f'symbol number {sybol_count}')
        if sybol_count > 5:
            break

    for i in range(len(yahoo_finance_scheduler_count)):
        symbol_queue.put('DONE')

    #for i in range(len(pg_scheduler_count)):
     #   out_queue.put('DONE')

    print(f'Running threads {len(yahoo_finance_scheduler_count)}')
    for i in range(len(yahoo_finance_scheduler_count)):
        yahoo_finance_scheduler_count[i].join()

    print(f'Running PG threads {len(pg_scheduler_count)}')
    for i in range(len(pg_scheduler_count)):
        pg_scheduler_count[i].join()


    print(f'Running threads {len(yahoo_finance_scheduler_count)}')
    print("Execution_time: ", round((time.time() - current_time)/1, 2))


if __name__ == "__main__":
    main()
