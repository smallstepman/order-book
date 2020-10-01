# Order book

## not implemented
- if two orders have same price, insert to list sorted by time added - "W przypadku takich samych cen decyduje czas dodania zlecenia, tzn. sortujemy rosnąco po czasie dodania zlecenia."
- Iceberg - "Opis działania zleceń typu Góra Lodowa znajdują się we wskazanym dokumencie."
    - multiple icebergs at same price point
    - aggressing order bigger than iceberg's peak
    - combinations of above two points 


## install
prerequisites: `pip install pipenv`
```
git clone https://github.com/marcinliebiediew/order_book
cd order_book
pipenv install
```
## run
```
pipenv run python src/app.py
```
or 
```
pipenv run python src/app.py ./tests/test_data/1.in
```
## test (TBA - damn import errors)
```
pipenv run pytest
```