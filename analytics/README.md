# Поиск

Общий пайплайн такой:

1. Запускаем парсер, он скачивает документы
2. Переносим все скаченное в csv

```
python manage.py model2csv accounts.WebPage > data.csv
```

3. Запускаем индексацию контента через `generate_search.py`

```
python generate_search.py --path data.csv
```

Появится файлик search.pkl, с ним работать так:

```
search_engine = pickle.load(open('search.pkl', 'rb'))
search_engine.search('банк')
```

Вернется что-то вроде:

```
[('https://cbr.ru/banking_sector/credit/FullCoList/@11697539444930777929',
  0.15355627043642192),
 ('https://cbr.ru/registries/nps/oper_zip/@11990872770296143492',
  0.14696566609751535),
 ('https://cbr.ru/hd_base/infodirectrepousd/@17865824223772606500',
  0.1383504373952472),
 ('https://cbr.ru/banking_sector/credit/coinfo/?id=350000004@9958357458796590883',
  0.1383504373952472),
 ('https://cbr.ru/hd_base/infodirectreporub/@3087914180279970663',
  0.13226909948776383),
 ('https://cbr.ru/hd_base/bankpapers/@16027420484538685728',
  0.11222832683810263),
 ('https://cbr.ru/banking_sector/credit/coinfo/?id=460000022@9579957001126118664',
  0.10287596626826073),
 ('https://cbr.ru/banking_sector/credit/coinfo/?id=450000203@11681252705765210661',
  0.10287596626826073),
 ('https://cbr.ru/analytics/insideinfo/@14438311283264946717',
  0.10287596626826073),
 ('https://cbr.ru/analytics/insideinfo/@431226185384911881',
  0.10287596626826073)]
```