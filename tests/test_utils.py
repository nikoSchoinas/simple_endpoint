"""
Tests for the functions inside utils.py
"""
import pytest
# Import modules from one directory  back
import sys
sys.path.insert(1, '..')
import utils

@pytest.mark.parametrize('arg, expected',
                         [('2023-01-01', True),
                          ('2019-05-23', True),
                          ('200-01-03', False),
                          ('2023-02-30', False)
                          ])
def test_is_date_valid(arg, expected):
    assert utils.is_date_valid(arg) == expected


@pytest.mark.parametrize('arg, expected',
                         [('order_id', True),
                          ('product_id', True),
                          ('product_description', True),
                          ('product_vat_rate', True),
                          ('discount_rate', True),
                          ('quantity', True),
                          ('full_price_amount', True),
                          ('discounted_amount', True),
                          ('vat_amount', True),
                          ('total_amount', True),
                          ('id', True),
                          ('created_at', True),
                          ('vendor_id', True),
                          ('customer_id', True),
                          ('date', True),
                          ('promotion_id', True),
                          ('Order_ID', False),
                          ('Product_ID', False)
                          ])
def test_is_column_name_valid(arg, expected):
    assert utils.is_column_name_valid(arg) == expected

@pytest.mark.parametrize('arg, expected',
                         [('Order', True),
                          ('OrderLine', True),
                          ('Promotion', True),
                          ('ProductPromotion', True),
                          ('VendorCommission', True),
                          ('order', False),
                          ('orderLine', False),
                          ('promotion', False),
                          ('productPromotion', False),
                          ('vendorCommission', False)
                          ])
def test_is_object_valid(arg, expected):
    assert utils.is_object_valid(arg) == expected


# Check if Exceptions are thrown
@pytest.mark.parametrize('arg1, arg2, arg3',
                         [('2019-08-01', 'CREATED_AT', 'Order'), # Invalid column_name
                          ('2019-08-01', 'created_at', 'ORDER') # Invalid object_name
                          ])
def test_filter_csv(arg1, arg2, arg3):
    with pytest.raises(NameError) as e:
        utils.filter_csv(arg1,arg2,arg3)
    assert e.match('Input fields are not valid')

# TODO is essential to write tests with
# fake data to check if the endpoint performs as it should



