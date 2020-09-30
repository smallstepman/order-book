from typing import Dict
import json
import bisect

from orders import OrderInputSchema, IcebergOrder, LimitOrder


class OrderBook:
    order_ids = []
    buy_orders = []
    sell_orders = []

    def __repr__(self):
        return json.dumps({
            'buyOrders': [o.overview() for o in self.buy_orders],
            'sellOrders': [o.overview() for o in self.sell_orders]
        })

    def new_order(self, raw_order: str) -> None:
        order_schema = OrderInputSchema()
        # if (v := order_schema.validate(raw_order)):
        #     print(v, raw_order)
        #     raise Exception(v)
        order = order_schema.loads(raw_order)
        if order.order_id in self.order_ids:
            raise Exception("duplicate order ID")
        self.order_ids.append(order.order_id)

        if order.direction.lower() == 'buy':
            if len(self.buy_orders) == 0:
                self.buy_orders.append(order)
            else:
                for i, e in enumerate(self.buy_orders):
                    if e.price <= order.price:
                        self.buy_orders.insert(i, order)
                        break
        elif order.direction.lower() == 'sell':
            bisect.insort(self.sell_orders, order)

    def make_transactions(self) -> None:
        transactions = []
        depleated = False
        while not depleated:

            for bo in self.buy_orders:

                for so in self.sell_orders:
                    if bo < so:
                        break
                    elif isinstance(so, IcebergOrder) and isinstance(bo, IcebergOrder):
                        print(bo.debug(), '\n', so.debug(), '\n')
                    elif isinstance(bo, IcebergOrder):
                        print(bo.debug(), '\n', so.debug(), '\n')
                    elif isinstance(so, IcebergOrder):
                        print(bo.debug(), '\n', so.debug(), '\n')
                    else:
                        print(bo.debug(), '\n', so.debug(), '\n')

            if True:
                depleated = True
                for t in transactions:
                    print(t)
