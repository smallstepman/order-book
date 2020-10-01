import json
import bisect
from typing import Dict, List, Union

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

    def make_transactions(self) -> List[Dict]:
        transactions = []

        for bo_idx, bo in enumerate(self.buy_orders):
            if len(self.sell_orders) >= 1:
                if bo < self.sell_orders[0]:
                    break

            for so_idx, so in enumerate(self.sell_orders):
                if bo > so:
                    if bo.quantity < so.quantity:
                        quantity_sold = bo.quantity
                        print(quantity_sold)
                        self.buy_orders[bo_idx].quantity = bo.quantity - \
                            quantity_sold
                        self.sell_orders[so_idx].quantity = so.quantity - \
                            quantity_sold
                    else:
                        quantity_sold = bo.quantity - so.quantity
                        self.buy_orders[bo_idx].quantity = bo.quantity - \
                            quantity_sold
                        self.sell_orders[so_idx].quantity = so.quantity - \
                            quantity_sold

                    transactions.append({
                        "buyOrderId": bo.order_id,
                        "sellOrderId": so.order_id,
                        "price": bo.price,
                        "quantity": quantity_sold
                    })

                    if bo.quantity == 0:
                        self.buy_orders.remove(bo)
                    if so.quantity == 0:
                        self.sell_orders.remove(so)

        return transactions
