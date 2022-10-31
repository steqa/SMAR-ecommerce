import datetime
import pytz
from store.models import Order
from ecommerce.settings import TIME_ZONE


def is_valid_queryparam(param):
    return param != '' and param is not None


def is_valid_sortparam(param):
    return param == '0' or param == '1' or param == '2'


def get_orders_chart_year_data():
    tz = pytz.timezone(TIME_ZONE)
    datetime_now = datetime.datetime.now(tz)
    orders = Order.objects.filter(date_ordered__year=datetime_now.year, status=3)
    orders_chart_year_data = {}
    for month in range(1, 13):
        filtered_orders = orders.filter(date_ordered__month=month)
        if filtered_orders:
            orders_chart_year_data[month] = filtered_orders
        else:
            orders_chart_year_data[month] = None
            
    return orders_chart_year_data


def get_chart_data(datatype):
    orders_chart_year_data = get_orders_chart_year_data()
    data = []
    for orders in orders_chart_year_data.values():
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