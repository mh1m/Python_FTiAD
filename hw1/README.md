# Рекурсивный парсер ссылок с заданной глубиной обхода
Параметры запуска: python web_crawler.py url n_depth \
url -- ссылка, n_depth -- глубина обхода \
При n_depth=0, будет скачан html-код передаваемой ссылки, при n_depth=1 html-код всех ссылок на передаваемой url, и т.д.

Пример запуска: python web_crawler.py https://stackoverflow.com 2
