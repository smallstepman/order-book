import json
import operator
from itertools import chain
from typing import Dict, List, Union, NewType

from orders import OrderInputSchema, IcebergOrder, LimitOrder


class OrderBook:

    _order_ids = []
    _OrderTypes = NewType('orders_types', Union[IcebergOrder, LimitOrder])
    _OrdersList = NewType('orders_list', List[_OrderTypes])
    _buy_orders = _OrdersList([])
    _sell_orders = _OrdersList([])

    def __repr__(self):
        return json.dumps({
            'buyOrders': [o.overview() for o in self._buy_orders],
            'sellOrders': [o.overview() for o in self._sell_orders]
        })

    def __str__(self):
        """ debug view """
        return json.dumps({
            'buyOrders': [o.debug() for o in self._buy_orders],
            'sellOrders': [o.debug() for o in self._sell_orders]
        })

    def new_order(self, raw_order: str) -> None:
        order_schema = OrderInputSchema()
        order = order_schema.loads(raw_order)
        if order.order_id in self._order_ids:
            raise Exception("duplicate order ID")
        self._order_ids.append(order.order_id)
        self._insort_order(order)

        transactions = []
        opposing_orders = self._sell_orders if order.direction == 'buy' else self._buy_orders
        if (ars := self._check_if_multiple_icebergs_at_same_price_point(order, opposing_orders)):
            transactions = self._multiple_icebergs_upahead(ars, order)
        else:
            for oo_idx, oo in enumerate(opposing_orders):
                just_executed = self._find_and_execute_transactions(oo)
                transactions = list(chain(just_executed + transactions))

        return transactions

    def _insort_order(self, new_order):
        if new_order.direction == 'buy':
            cmp, orders_list = False, operator.gt, self._buy_orders
        elif new_order.direction == 'sell':
            cmp, orders_list = True, operator.lt, self._sell_orders
        insert_here = False

        orders_list.append(new_order)
        orders_list.sort(key=lambda i: (
            i.price, i.timestamp), reverse=not r)

    def make_transactions(self) -> List[Dict]:
        transactions = []

        # aweful time complexity, maybe could be reduced with dynamic programming approach but I'm not that smart yet
        for bo_idx, bo in enumerate(self._buy_orders):
            if (l := self._check_if_multiple_orders_at_same_price_point(bo, self._sell_orders)):
                transactions = self._multiple_icebergs_upahead(bo, l)
            else:
                just_executed_transactions = self._find_and_execute_transactions(
                    bo)
                transactions = list(itertools.chain(
                    just_executed_transactions + transactions))

        return transactions

    # def _check_if_multiple_icebergs_at_same_price_point(self, order, orders_list):
    #     return [i for i, other in enumerate(orders_list) if order == other and isinstance(other, IcebergOrder)]
    #     # if any(same_price_icebergs_idx):

    # def _multiple_icebergs_upahead(self, idxs: List[int], aggressing_order: _OrderTypes):
    #     iceberg_orders = []
    #     t = []
    #     ao_dir = ''
    #     if aggressing_order.direction == 'buy':
    #         ao_dir = "buy"
    #         for i in idxs:
    #             iceberg_orders.append(self._sell_orders[i])
    #     if aggressing_order.direction == 'sell':
    #         ao_dir = "buy"
    #         for i in idxs:
    #             iceberg_orders.append(self._buy_orders[i])

    #     icebergs_total_visible_quantity = sum(o.quantity for o in iceberg_orders)
    #     icebergs_total_hidden_quantity = sum(
    #         o.hidden_quantity for o in iceberg_orders)
    #     aggressing_order_total_quantity = aggressing_order.quantity + aggressing_order.hidden_quantity
    #     aggressing_order_quantity_left_after_consuming_peaks = aggressing_order_total_quantity - \
    #         icebergs_total_visible_quantity
    #     if icebergs_total_visible_quantity >= aggressing_order_total_quantity:
    #         for io in iceberg_orders:
    #             t.append(self._execute_transaction(io, aggressing_order))
    #     else:
    #         for io in iceberg_orders:
    #             qualtity_sold = io.hidden_quantity / \
    #                 total_hidden_quantity * aggressing_order_quantity_left_after_consuming_peaks
    #             t.append(self._execute_transaction(io, aggressing_order))
    #             io.hidden_quantity -= qualtity_sold
    #             aggressing_order.hi

    #     return t

    def _execute_transaction(self, order, opposite_order):
        if order.quantity <= opposite_order.quantity:
            quantity_sold = order.quantity
        else:
            quantity_sold = order.quantity - opposite_order.quantity

        order.quantity -= quantity_sold
        opposite_order.quantity -= quantity_sold

        self._update_order_after_transaction(order)
        self._update_order_after_transaction(opposite_order)

        return {
            "buyOrderId": order.order_id if order.direction == 'buy' else opposite_order.order_id,
            "sellOrderId": order.order_id if order.direction == 'sell' else opposite_order.order_id,
            "price": opposite_order.price,
            "quantity": quantity_sold
        }

    def _find_and_execute_transactions(self, buy_order, t=[]):
        for so_idx, sell_order in enumerate(self._sell_orders):
            if buy_order >= sell_order:

                if buy_order.quantity <= sell_order.quantity:
                    quantity_sold = buy_order.quantity
                else:
                    quantity_sold = buy_order.quantity - sell_order.quantity

                buy_order.quantity -= quantity_sold
                sell_order.quantity -= quantity_sold

                self._update_order_after_transaction(buy_order)
                self._update_order_after_transaction(sell_order)

                t.append({
                    "buyOrderId": buy_order.order_id,
                    "sellOrderId": sell_order.order_id,
                    "price": buy_order.price,
                    "quantity": quantity_sold
                })

                if buy_order.quantity > 0:
                    if isinstance(buy_order, IcebergOrder):
                        # print(buy_order.debug())
                        t = self._find_and_execute_transactions(buy_order, t)

        return t

    def _update_order_after_transaction(self, order: _OrderTypes):
        if order.quantity == 0:
            if isinstance(order, IcebergOrder):
                if order.hidden_quantity > order.peak:
                    order.quantity = order.peak
                    order.hidden_quantity -= order.peak
                elif order.hidden_quantity == 0 and order.quantity == 0:
                    self._delete_order_with_zero_quantity(order)
                else:
                    order.quantity = order.hidden_quantity
                    order.hidden_quantity = 0
            else:
                self._delete_order_with_zero_quantity(order)

    def _delete_order_with_zero_quantity(self, order):
        if order.direction == 'buy':
            idx = self._buy_orders.index(order)
            self._buy_orders.pop(idx)
        elif order.direction == 'sell':
            idx = self._sell_orders.index(order)
            self._sell_orders.pop(idx)
