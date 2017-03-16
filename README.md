# SE_dump_parser
Python parser for StackExchange xml dump (https://archive.org/details/stackexchange)

Как использовать:
- скачать дамп нужной категории с https://archive.org/details/stackexchange
- запустить скрипт: python parse_SE_dump.py -f dump_filename
 
Результатом будет csv файл с выгруженными данными. Формат строки "вопрос" - "ответ". Если на текущий вопрос было несколько ответом, то формируются строки данных для каждого ответа.

Полученный датасет может быть использован для целей NLP (для некоторых целей сделан padding пунктуации пробелами)
