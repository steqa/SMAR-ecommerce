import datetime
import pytz
from store.models import Order
from ecommerce.settings import TIME_ZONE
from calendar import monthrange
from django.http.response import JsonResponse
from django.template.loader import render_to_string


def is_valid_queryparam(param):
    return param != '' and param is not None


def is_valid_sortparam(param):
    return param == '0' or param == '1' or param == '2'


def render_chart_data(request):
    period = request.GET.get('period')
    selected_year = request.GET.get('selected_year')
    selected_month = request.GET.get('selected_month')
    chart_type = request.GET.get('chart_type')
    tz = pytz.timezone(TIME_ZONE)
    datetime_now = datetime.datetime.now(tz)

    if period == 'month':
        selected_year = int(selected_year)
        selected_month = int(selected_month)
    elif period == 'year':
        selected_year = int(selected_year)
        selected_month = None
    elif period == 'all_years':
        selected_year = None
        selected_month = None
    else:
        period = 'year'
        selected_year = datetime_now.year
        selected_month = None
    
    if chart_type == 'sales':
        chart_data = get_chart_data(datatype='sales', period=period, year=selected_year, month=selected_month)
    elif chart_type == 'revenue':
        chart_data = get_chart_data(datatype='revenue', period=period, year=selected_year, month=selected_month)
    
    orders_by_year = get_orders_by_period(period='year', year=selected_year, month=selected_month)['orders_by_period']
    orders_by_all_years = get_orders_by_period(period='all_years', year=selected_year, month=selected_month)['orders_by_period']

    context = {
        'orders_by_year': orders_by_year,
        'orders_by_all_years': orders_by_all_years,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'chart_type': chart_type,
    }
    return JsonResponse({
      'html': render_to_string('sales_dashboard/chart.html', context, request),
      'period': period,
      'chart_data': chart_data,
    })


def get_orders_by_period(period, year, month):
    data = {}
    tz = pytz.timezone(TIME_ZONE)
    datetime_now = datetime.datetime.now(tz)
    if period == 'all_years':
        orders = Order.objects.filter(status=3)
        period_range = range(2004, datetime_now.year + 1)
    elif period == 'year':
        orders = Order.objects.filter(date_ordered__year=year, status=3)
        period_range = range(1, 13)
    elif period == 'month':
        orders = Order.objects.filter(date_ordered__year=year, date_ordered__month=month, status=3)
        period_range = range(1, monthrange(year, month)[1] + 1)
    
    data['period_range'] = [p for p in period_range]
    orders_by_period = {}
    for p in period_range:
        if period == 'all_years':
            filtered_orders = orders.filter(date_ordered__year=p)
        elif period == 'year':
            filtered_orders = orders.filter(date_ordered__year=year, date_ordered__month=p)
        elif period == 'month':
            filtered_orders = orders.filter(date_ordered__year=year, date_ordered__month=month, date_ordered__day=p)
            
        if filtered_orders:
            orders_by_period[p] = filtered_orders
        else:
            orders_by_period[p] = None
        
    data['orders_by_period'] = orders_by_period
    return data

def get_chart_data(datatype, period, year, month):
    orders_by_period_data = get_orders_by_period(period=period, year=year, month=month)
    orders_by_period = orders_by_period_data['orders_by_period']
    period_range = orders_by_period_data['period_range']
    returned_data = {}
    returned_data['labels'] = period_range
    data = []
    for orders in orders_by_period.values():
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
    
    returned_data['data'] = data
    returned_data['type'] = datatype
    return returned_data