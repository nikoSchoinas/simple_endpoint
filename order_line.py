"""
The class OrderLine
"""
class OrderLine:
    def __init__(self, order_id, product_id, product_description, product_price,
                 product_vat_rate, discount_rate, quantity, full_price_amount,
                 discounted_amount, vat_amount, total_amount):
        self.order_id = order_id
        self.product_id = product_id
        self.product_description = product_description
        self.product_price = product_price
        self.product_vat_rate = product_vat_rate
        self.discount_rate = discount_rate
        self.quantity = quantity
        self.full_price_amount = full_price_amount
        self.discounted_amount = discounted_amount
        self.vat_amount = vat_amount
        self.total_amount = total_amount