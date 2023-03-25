"""
A collection of function that helps perform various tasks such validation, calculating the means etc
"""

import datetime
import pandas as pd
from order import Order
from order_line import OrderLine
from product import Product
from promotion import Promotion
from product_promotion import ProductPromotion
from vendor_commission import VendorCommission
import utils

def is_date_valid(date_str):
    """
    Check if the date format is valid.

    Parameters
    ----------
    date_str : str
        The date in format YYYY-MM-DD
    
    Returns
    -------
    : bool
    True/False if the date is valid/not-valid
    """
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def is_column_name_valid(column_name):
    """
    Check if the column_name is valid.

    Parameters
    ----------
    column_name : str
        The column name as appeared in CSVs
    
    Returns
    -------
    : bool
    True/False if the column_name is valid/not-valid
    """
    if column_name in ['order_id', 'product_id', 'product_description',
                       'product_price', 'product_vat_rate', 'discount_rate',
                       'quantity', 'full_price_amount', 'discounted_amount',
                       'vat_amount', 'total_amount', 'id', 'created_at',
                       'vendor_id', 'customer_id', 'date', 'promotion_id',
                       'description', 'rate']:
        return True
    else:
        return False
    
def is_object_valid(object_name):
    """
    Check if the object_name is valid.

    Parameters
    ----------
    object_name : str
        One of the objects, e.g. Order, Product etc
    
    Returns
    -------
    : bool
    True/False if the object_name is valid/not-valid
    """
    if object_name in ['Order', 'OrderLine', 'Product', 'Promotion', 'ProductPromotion', 'VendorCommission']:
        return True
    else:
        return False



def filter_csv(filter_value, column_name, object_name):
    """
    Reads a csv and filters its rows based on a column condition.

    Parameters
    ----------
    filter_value : str
        The column value for which to perform the filtering
    column_name : str
        The name of the CSV column to perform the condition.
    object_name : str
        The object that needs to be created, e.g. Order, OrderLine, Product etc
    
    Returns
    -------
    : list(Object)
        The list with the right objects for a given date.
    
    Raises
    ------
    NameError if the input fields are not valid.
    """
    # Validate input fields
    if not is_column_name_valid(column_name) or not is_object_valid(object_name):
        raise NameError('Input fields are not valid')
    # Read the right CSV file.
    if object_name == 'Order':
        csv = pd.read_csv('data/orders.csv')
    elif object_name == 'OrderLine':
        csv = pd.read_csv('data/order_lines.csv')
    elif object_name == 'Product':
        csv = pd.read_csv('data/products.csv')
    elif object_name == 'Promotion':
        csv = pd.read_csv('data/promotions.csv')
    elif object_name == 'ProductPromotion':
        csv = pd.read_csv('data/product_promotions.csv')
    elif object_name == 'VendorCommission':
        csv = pd.read_csv('data/commissions.csv')

    # Filter the DataFrame to only include rows where the column_name column contains the date_str
    filtered_csv= csv[csv[column_name].astype(str).str.contains(filter_value)]
    # Create the list with the right objects
    # Read the right CSV file.
    if object_name == 'Order':
        return [Order(id=row['id'], created_at=row['created_at'],
                      vendor_id=row['vendor_id'], customer_id=row['customer_id']) for index, row in filtered_csv.iterrows()]
    elif object_name == 'OrderLine':
        return [OrderLine(order_id=row['order_id'], product_id=row['product_id'],
                          product_description=row['product_description'], product_price=row['product_price'],
                          product_vat_rate=row['product_vat_rate'], discount_rate=row['discount_rate'],
                          quantity=row['quantity'], full_price_amount=row['full_price_amount'],
                          discounted_amount=row['discounted_amount'], vat_amount=row['vat_amount'],
                          total_amount=row['total_amount']) for index, row in filtered_csv.iterrows()]
    elif object_name == 'Product':
        return [Product(id=row['id'], description=row['description']) for index, row in filtered_csv.iterrows()]
    elif object_name == 'Promotion':
        return [Promotion(id=row['id'], description=row['description']) for index, row in filtered_csv.iterrows()]
    elif object_name == 'ProductPromotion':
        return [ProductPromotion(date=row['date'], product_id=row['product_id'],
                                 promotion_id=row['promotion_id']) for index, row in filtered_csv.iterrows()]
    elif object_name == 'VendorCommission':
        return [VendorCommission(date=row['date'], vendor_id=row['vendor_id'],
                                  rate=row['rate']) for index, row in filtered_csv.iterrows()]
    # In case everything fails return an empty list
    return []


def get_vendor_rate(commissions, vendor_id):
    """
    Finds the vendor commission rate given the commissions for a date and the vendor's id

    Parameters
    ----------
    commissions : list(VendorCommission)
        A list containing the commissions for a specific date.
    vendor_id : str
        The vendor's id to get the commission rate.
    
    Returns
    -------
    : int
        The commission rate of the vendor. 
    """
    for commission in commissions:
        if commission.vendor_id == vendor_id:
            return commission.rate

def get_promotion_id(product_promotions, product_id):
    """
    Finds the promotion id given the product promotions for a date and the product id

    Parameters
    ----------
    product_promotions : list(ProductPromotions)
        A list containing the product promotions for a specific date.
    product_id : str
        The product's id to get the promotion id.
    
    Returns
    -------
    : int
        The promotion id. 
    """
    for promotion in product_promotions:
        if promotion.product_id == product_id:
            return promotion.promotion_id
    # If the promotion does not exist return 0
    return 0


def initialise_endpoint():
    """
    Initialise all the keys for the endpoint dictionary
    """
    return {
        'customers': 0,
        'total_discount_amount': 0,
        'items': 0,
        'order_total_avg': 0,
        'discount_rate_avg': 0,
        'commissions': {
            'promotions': {
                '1': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0
            },
            'total': 0,
            'order_average': 0
        }
    }


def create_endpoint(date_str):
    """
        Creates the endpoint with all the information.

        Parameters
        ----------
        date_str : str
            The date in format YYYY-MM-DD
        
        Returns
        -------
        endpoint: dict
            The dictionary that includes all the information
    """
    endpoint = initialise_endpoint()
    # The total number of items sold on that day.
    orders = utils.filter_csv(date_str, 'created_at', 'Order')
    endpoint['items'] = len(orders)

    # The total number of customers that made an order that day.
    customers = [order.customer_id for order in orders]
    endpoint['customers'] = len(set(customers))

    commissions = utils.filter_csv(date_str, 'date', 'VendorCommission')
    product_promotions = utils.filter_csv(date_str, 'date', 'ProductPromotion')

    order_ids = list(set([order.id for order in orders]))
    vendor_ids = list(set([order.vendor_id for order in orders]))

    # The total amount of discount given that day
    discount = 0
    # The average discount rate applied to the items sold that day
    discount_rate = 0
    num_discount_rate = 0
    # The average order total for that day
    order_total = 0
    num_order_total = 0
    # The total amount of commissions generated that day
    total_commission = 0

    for id, vendor_id in zip(order_ids, vendor_ids):
        # For every order id read the order_lines
        order_lines = utils.filter_csv(str(id), 'order_id', 'OrderLine')

        tmp_discount = [line.discounted_amount for line in order_lines]
        # The average discount rate applied to the items sold that day
        tmp_discount_rate = [line.discount_rate for line in order_lines]

        tmp_order_total = [line.total_amount for line in order_lines]
        discount += sum(tmp_discount)
        discount_rate += sum(tmp_discount_rate)
        num_discount_rate += len(tmp_discount_rate)
        order_total += sum(tmp_order_total)
        num_order_total += len(tmp_order_total)
        vendor_rate = get_vendor_rate(commissions, vendor_id)
        total_commission += num_order_total * vendor_rate

        # The total amount of commissions earned per promotion that day
        for line in order_lines:
            promotion_id = get_promotion_id(product_promotions, line.product_id)
            # Check if the product id is part of a promotion.
            if promotion_id:
                endpoint['commissions']['promotions'][str(promotion_id)] += line.total_amount * vendor_rate

    endpoint['total_discount_amount'] = discount
    endpoint['discount_rate_avg'] = discount_rate / num_discount_rate if num_discount_rate != 0 else 0
    endpoint['order_total_avg'] = order_total / num_order_total if num_order_total != 0 else 0
    endpoint['commissions']['total'] = total_commission
    # The average amount of commissions per order for that day.
    endpoint['commissions']['order_average'] = total_commission / len(orders) if len(orders) != 0 else 0


    return endpoint














