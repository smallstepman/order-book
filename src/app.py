import sys

from order_book import OrderBook

book = OrderBook()

if len(sys.argv) > 1:
    with open(sys.argv[1], mode='r') as f:
        f.readlines()
else:
    while True:
        try:
            # input_order_raw = input()
            # book.new_order(input_order_raw)
            [book.new_order(o) for o in [
                """{"type": "Limit", "order": {"direction": "Buy", "id": 1, "price": 14, "quantity": 20}}""",
                """{"type": "Iceberg", "order": {"direction": "Buy", "id": 2, "price": 15, "quantity": 50, "peak": 20}}""",
                """{"type": "Limit", "order": {"direction": "Sell", "id": 3, "price": 16, "quantity": 15}}""",
                """{"type": "Limit", "order": {"direction": "Sell", "id": 4, "price": 13, "quantity": 60}}""",
                """{"type": "Limit", "order": {"direction": "Sell", "id": 6, "price": 13, "quantity": 60}}"""
            ]]
            print(book)
        except Exception as e:
            break
            print(e.args)
        book.make_transactions()
