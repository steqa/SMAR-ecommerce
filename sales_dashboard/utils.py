import datetime
import pytz
from store.models import Order
from ecommerce.settings import TIME_ZONE


def is_valid_queryparam(param):
    return param != '' and param is not None


def is_valid_sortparam(param):
    return param == '0' or param == '1' or param == '2'


def get_orders_by_period(period):
    tz = pytz.timezone(TIME_ZONE)
    datetime_now = datetime.datetime.now(tz)
    if period == 'year':
        orders = Order.objects.filter(date_ordered__year=datetime_now.year, status=3)
        period_range = range(1, 13)
    elif period == 'all_years':
        orders = Order.objects.filter(status=3)
        period_range = range(2004, datetime_now.year + 1)
        
    orders_by_period = {}
    for p in period_range:
        if period == 'year':
            filtered_orders = orders.filter(date_ordered__month=p)
        elif period == 'all_years':
            filtered_orders = orders.filter(date_ordered__year=p)
            
        if filtered_orders:
            orders_by_period[p] = filtered_orders
        else:
            orders_by_period[p] = None
            
    return orders_by_period

def get_chart_data(datatype, period):
    orders_chart_months_data = get_orders_by_period(period)
    data = []
    for orders in orders_chart_months_data.values():
        if orders is not None:
            orders_data = 0
            for order in orders:
                if datatype == 'sales':
                    orders_data += 1
                elif datatype == 'revenue':
                    orders_data += int(order.get_total_order_price)
            data.append(orders_data)
        else:
            data.append(0)
            
    return data