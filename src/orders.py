from datetime import datetime

from marshmallow import fields, Schema, validates, ValidationError, post_load


class OrderDetailsSchema(Schema):
    id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    price = fields.Integer(required=True)
    direction = fields.Str(required=True)
    peak = fields.Integer()

    @validates('direction')
    def check_order_type(self, value):
        if value.lower() not in ['buy', 'sell']:
            ValidationError("unsupported order direction")


class OrderInputSchema(Schema):
    type = fields.Str(required=True)
    order = fields.Nested(OrderDetailsSchema, required=True)

    @validates('type')
    def check_order_type(self, value):
        if value.lower() not in ['limit', 'iceberg']:
            ValidationError("unsupported order type")

    @post_load
    def make_order(self, data, **kwargs):
        if (t := data['type'].lower()) == 'limit':
            return LimitOrder(**data['order'])
        elif t == 'iceberg':
            return IcebergOrder(**data['order'])


class Order:
    def __lt__(self, other):
        return self.price < other.price

    def __le__(self, other):
        return self.price <= other.price

    def __eq__(self, other):
        return self.price == other.price

    def __ne__(self, other):
        return self.price != other.price

    def __ge__(self, other):
        return self.price >= other.price

    def __gt__(self, other):
        return self.price > other.price

    def overview(self):
        return dict(
            id=self.order_id, quantity=self.quantity(), price=self.price
        )

    def debug(self):
        return str(self.__dict__)


class LimitOrder(Order):
    order_id = None
    quantity = None
    price = None
    direction = None
    timestamp = None

    def __init__(self, id, quantity, price, direction):
        self.order_id = id
        self.quantity = quantity
        self.price = price
        self.direction = direction.lower()
        self.timestamp = datetime.now()

    def quantity(self):
        return self.quantity


class IcebergOrder(Order):
    order_id = None
    quantity = None
    price = None
    direction = None
    peak = None
    hidden_quantity = None
    start_quantity = None
    timestamp = None

    def __init__(self, id, quantity, price, direction, peak):
        self.order_id = id
        self.quantity = peak
        self.price = price
        self.direction = direction.lower()
        self.peak = peak
        self.hidden_quantity = quantity - peak
        self.start_quantity = quantity
        self.timestamp = datetime.now()

    # # @classmethod
    # def quantity(self):
    #     if self.peak < self.total_quantity:
    #         return self.peak
    #     else
