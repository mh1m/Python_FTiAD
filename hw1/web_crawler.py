import os
import re
import sys
import shutil
import requests

from collections import OrderedDict
from bs4 import BeautifulSoup


class WebCrawler(object):
    """
    Класс для парсинга ссылок c заданной глубиной

    """

    def __init__(self):
        self.index = 1
        self.visited_urls = set()
        self.errors = OrderedDict()

    @staticmethod
    def _create_data_folder_and_txt():
        """
        Метод создает папку data и файл urls.txt в директории программы

        """
        path = os.getcwd()
        data_path = os.path.join(path, 'data')
        if os.path.isdir(data_path):
            shutil.rmtree(data_path)
        os.mkdir(data_path)
        txt_path = os.path.join(path, 'urls.txt')
        f = open(txt_path, "w")
        f.close()

    @staticmethod
    def _write_to_file(path: str, value):
        """
        Сохранение объекта в файл

        """
        with open(path, 'w') as f:
            f.write(str(value))

    @staticmethod
    def _get_links_from_soup(soup: 'BeautifulSoup') -> list:
        """
        Сбор ссылок с html-кода

        """
        links = []
        soup_links = soup.find_all(attrs={'href': re.compile("http")})
        for link in soup_links:
            links.append(link.get('href'))
        return links

    def get_html(self, url: str) -> str | None:
        """
        Получение html-кода страницы

        """
        try:
            r = requests.get(url)
        except (ConnectionError,
                requests.exceptions.ConnectionError,
                requests.exceptions.MissingSchema,
                requests.exceptions.InvalidSchema) as exception:
            self.errors[url] = str(exception)
            return
        return r.text

    def _write_to_txt(self, url: str):
        """
        Метод делеает записть в файл urls.txt.
        Запись представленна в виде 'index url'.
        Пример:
        1 https://ya.ru
        2 https://yandex.ru

        """
        with open("urls.txt", "a") as file:
            file.write(f"{self.index} {url}\n")


    def web_crawler(self, url: str, n_depth: int):
        """
        Метод получает на вход ссылку и глубину обхода
        Глубина обхода (n_depth) равна 0, если мы хотим получить
        html входного значения url, если n_depth=1,
        тогда будут получены все html ссылкок, находящихся на url.
        Таким образом, получается рекурсивный алгоритм получения html-страниц.

        """
        if n_depth == -1:
            return
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        html = self.get_html(url)
        if html is None:
            return
        soup = BeautifulSoup(html, features="lxml")
        self._write_to_txt(url)
        cwd = os.getcwd()
        path = os.path.join(cwd, 'data', f'{self.index}.html')
        self._write_to_file(path, soup)
        self.index += 1
        links = self._get_links_from_soup(soup)
        for link in links:
            self.web_crawler(link, n_depth-1)

    def parse(self, url: str, n_depth: int):
        """
        Основной метод парсинга

        """
        self._create_data_folder_and_txt()
        self.web_crawler(url, n_depth)

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    url = sys.argv[1]
    n_depth = int(sys.argv[2])
    web = WebCrawler()
    web.parse(url, n_depth)
