import time
import threading
from multiprocessing import Queue

from workers.WikiWorker import WikiWorker
from workers.YahooFinancePriceWorker import YahooFinanceScheduler


def main():
    symbol_queue = Queue()
    current_time = time.time()
    wiki_worker = WikiWorker()

    yahoo_finance_scheduler_num = 10

    yahoo_finance_scheduler_count = []
    for i in range(yahoo_finance_scheduler_num):
        yahoo_finance_scheduler = YahooFinanceScheduler(symbol_queue)
        yahoo_finance_scheduler_count.append(yahoo_finance_scheduler)

    for symbol in wiki_worker.get_500_companies():
        symbol_queue.put(symbol)

    for i in range(len(yahoo_finance_scheduler_count)):
        symbol_queue.put('DONE')
    #    yahoo_finance_worker = YahooFinanceWorker(symbol)
     #   my_workers.append(yahoo_finance_worker)

    print(f'Running threads {len(yahoo_finance_scheduler_count)}')
    for i in range(len(yahoo_finance_scheduler_count)):
        yahoo_finance_scheduler_count[i].join()

    print(f'Running threads {len(yahoo_finance_scheduler_count)}')
    print("Execution_time: ", round((time.time() - current_time)/1, 2))


if __name__ == "__main__":
    main()
