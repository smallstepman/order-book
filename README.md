# Order book

## not implemented:
- W przypadku takich samych cen decyduje czas dodania zlecenia, tzn. sortujemy rosnąco po czasie dodania zlecenia.
- Opis działania zleceń typu Góra Lodowa znajdują się we wskazanym dokumencie.

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
or (TBA)
```
pipenv run python src/app.py tests/test_data/1.in
```
## test
```
pipenv run pytest
```