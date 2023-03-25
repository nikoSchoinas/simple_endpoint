"""
The class Order
"""
class Order:
    def __init__(self, id, created_at, vendor_id, customer_id):
        self.id = id
        self.created_at = created_at
        self.vendor_id = vendor_id
        self.customer_id = customer_id