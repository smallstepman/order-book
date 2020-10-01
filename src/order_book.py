import json
import bisect
from typing import Dict, List, Union, NewType

from orders import OrderInputSchema, IcebergOrder, LimitOrder


class OrderBook:
    order_ids = []
    OrdersList = NewType('orders_list', List[Union[IcebergOrder, LimitOrder]])
    buy_orders = OrdersList([])
    sell_orders = OrdersList([])

    def __repr__(self):
        return json.dumps({
            'buyOrders': [o.overview() for o in self.buy_orders],
            'sellOrders': [o.overview() for o in self.sell_orders]
        })

    def new_order(self, raw_order: str) -> None:
        """
            not implemented:
            - if two orders have same price, insert to list sorted by time added 
        """
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
        """
            not implemented:
            - multiple icebergs at same price point
            - aggressing order bigger than iceberg's peak
            - combinations of above two points 
        """
        transactions = []

        # awefut time complexity, maybe could be reduced with dynamic programming approach but I'm not that smart yet
        for bo_idx, bo in enumerate(self.buy_orders):
            # break early - no valid transactions
            if len(self.sell_orders) >= 1:
                if bo < self.sell_orders[0]:
                    break

            for so_idx, so in enumerate(self.sell_orders):
                if bo > so:
                    if bo.quantity < so.quantity:
                        quantity_sold = bo.quantity
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

                    self._update_after_transaction(
                        idx=bo_idx, order=bo, orders_list=self.buy_orders)
                    self._update_after_transaction(
                        idx=so_idx, order=so, orders_list=self.sell_orders)

        return transactions

    # def _execute_transaction(bo, so):
    #     if bo.quantity < so.quantity:
    #         quantity_sold = bo.quantity
    #         self.buy_orders[bo_idx].quantity = bo.quantity - \
    #             quantity_sold
    #         self.sell_orders[so_idx].quantity = so.quantity - \
    #             quantity_sold
    #     else:
    #         quantity_sold = bo.quantity - so.quantity
    #         self.buy_orders[bo_idx].quantity = bo.quantity - \
    #             quantity_sold
    #         self.sell_orders[so_idx].quantity = so.quantity - \
    #             quantity_sold

    #     return {
    #         "buyOrderId": bo.order_id,
    #         "sellOrderId": so.order_id,
    #         "price": bo.price,
    #         "quantity": quantity_sold
    #     }

    def _update_after_transaction(self, idx: int, order: Union[IcebergOrder, LimitOrder], orders_list: OrdersList):
        if order.quantity == 0:
            if isinstance(order, IcebergOrder):
                if order.hidden_quantity > order.peak:
                    order.quantity = order.peak
                    order.hidden_quantity -= order.peak
                    # ???_execute_transaction()
                elif order.hidden_quantity == 0 and order.quantity == 0:
                    orders_list.pop(idx)
                else:
                    order.quantity = order.hidden_quantity
                    # ???_execute_transaction()
                    order.hidden_quantity = 0
            else:
                orders_list.pop(idx)
