import sys

from order_book import OrderBook

book = OrderBook()


def run_from_file(path):
    with open(path, mode='r') as f:
        orders = f.readlines()
        for o in orders:
            # try:
            o = o.strip('\n')
            if not (o.startswith('{') and o.endswith('}')):
                print(
                    f"is not a JSON object, (arrays of objects are not supported) \n{o}")
                exit()
            print(">", o)
            print("pre ", str(book))
            transactions = book.new_order(o)
            # except Exception as e:
            #     print(e.args)
            #     exit()

            # transactions = book.make_transactions()
            print("post", str(book))

            for t in transactions:
                print(t)
            print('\n')


def run_as_console():
    while True:
        try:
            input_order_raw = input("> ")
            if not (input_order_raw.startswith('{') and input_order_raw.endswith('}')):
                print("not a JSON object, (arrays of objects are not supported)")
                continue
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
