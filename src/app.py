import sys

from order_book import OrderBook

book = OrderBook()


def run_from_file(path):
    with open(path, mode='r') as f:
        orders = f.readlines()
        for o in orders:
            if o.startswith('-'):
                break
            try:
                book.new_order(o)
            except:
                print(e.args)
                exit()

            transactions = book.make_transactions()

            print(book)
            for t in transactions:
                print(t)


def run_as_console():
    i = 0

    while True:
        # try:
        # input_order_raw = input()
        # book.new_order(input_order_raw)

        d = [
            """{"type": "Limit", "order": {"direction": "Buy", "id": 1, "price": 14, "quantity": 20}}""",
            # """{"type": "Limit", "order": {"direction": "Buy", "id": 2, "price": 15, "quantity": 20}}""",
            # """{"type": "Limit", "order": {"direction": "Buy", "id": 9, "price": 15, "quantity": 20}}""",

            # # """{"type": "Iceberg", "order": {"direction": "Buy", "id": 2, "price": 15, "quantity": 50, "peak": 20}}""",
            # """{"type": "Limit", "order": {"direction": "Sell", "id": 3, "price": 16, "quantity": 15}}""",
            """{"type": "Limit", "order": {"direction": "Sell", "id": 4, "price": 13, "quantity": 10}}""",
            # """{"type": "Limit", "order": {"direction": "Sell", "id": 43, "price": 13, "quantity": 3}}""",

            # """{"type": "Limit", "order": {"direction": "Buy", "id": 5, "price": 13, "quantity": 60}}""",
            # """{"type": "Limit", "order": {"direction": "Sell", "id": 6, "price": 13, "quantity": 30}}""",

        ]
        print(">", d[i])

        book.new_order(d[i])
        i = i + 1
        # print(book)

        # except Exception as e:
        #     print(e.args)
        #     break

        transactions = book.make_transactions()

        print(book)
        for t in transactions:
            print(t)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_from_file(sys.argv[1])
    else:
        run_as_console()
