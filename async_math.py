import math
import multiprocessing
import time
import threading
from functools import wraps
from random import randrange

def time_manager(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f'Время выполнения функции {func.__name__}:'
              f' {(time.time() - start_time):.2f} s')
        return result
    return wrapper

dict_factorials = dict()


def append_factorials_to_dict(num: int):
    if num != 0:
        dict_factorials[f'num {num}'] = math.factorial(num)
    else:
        dict_factorials['num 0'] = 1

if __name__ == '__main__':


    """функции принимают лист чисел и возвращает дикт,
     где ключи это значения из сэта, а значения это факториалы чисел """

    @time_manager
    def list_to_factorial_dict(list_of_nums: list):
        for num in list_of_nums:
            append_factorials_to_dict(num)


    @time_manager
    def threading_list_to_factorial_dict(list_of_nums: list):
        threads = []
        for num in list_of_nums:
            thread = threading.Thread(target=append_factorials_to_dict, args=(num,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()


    @time_manager
    def multiprocessing_list_to_factorial_dict(list_of_nums: list):
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = pool.map(append_factorials_to_dict, list_of_nums)


    list_of_nums = [randrange(0, 100000) for _ in range(100)]
    list_to_factorial_dict(list_of_nums)
    threading_list_to_factorial_dict(list_of_nums)
    multiprocessing_list_to_factorial_dict(list_of_nums)

"""При больщих значениях randrange multiprocessing подход почти в два раза быстрее
threading незначительно быстрее линейного подхода"""