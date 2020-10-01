import sys

from order_book import OrderBook

book = OrderBook()


def run_from_file(path):
    with open(path, mode='r') as f:
        orders = f.readlines()
        for o in orders:
            try:
                book.new_order(o)
                print(">", o)
            except:
                print(e.args)
                exit()

            transactions = book.make_transactions()

            print(book)
            for t in transactions:
                print(t)


def run_as_console():
    while True:
        try:
            input_order_raw = input("> ")
            book.new_order(input_order_raw)
        except Exception as e:
            print(e.args)
            continue

        transactions = book.make_transactions()

        print(book)
        for t in transactions:
            print(t)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_from_file(sys.argv[1])
    else:
        run_as_console()
