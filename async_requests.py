import threading
import multiprocessing
from async_math import time_manager
import requests


def download_content(url):
    try:
        response = requests.get(url)
        return url, response.status_code
    except requests.RequestException as e:
        return (url, f'Произошла ошибка {e}')

if __name__ == '__main__':

    urls = [
        "https://lms.teachmeskills.com",
        "https://openai.com",
        "https://docs.djangoproject.com",
        "https://github.com",
        "https://google.com",
        "https://youtube.com",
    ]

    @time_manager
    def sync_fetch_urls(urls):
        for url in urls:
            content = download_content(url)
            print(f'Выполнен запрос {url}, результат запроса {content[1]}')


    @time_manager
    def threading_fetch_urls(urls):
        threads = []
        for url in urls:
            thread = threading.Thread(target=download_content, args=(url,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    @time_manager
    def multiprocessing_fetch_urls(urls):
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = pool.map(download_content, urls)
        for url, status in results:
            print(f'URL: {url}, Статус {status}')

    sync_fetch_urls(urls)
    threading_fetch_urls(urls)
    multiprocessing_fetch_urls(urls)

"""Здесь с отрывом выигрывает threading подход, разница почти в 4 раза
multiprocessing оказался в полтора раза медленне чем линейный подход
возможно из за создания большего кол-ва процессов которые я не ограничивал"""
