import datetime
import pytz
import json
from calendar import monthrange
from django.template.defaultfilters import date
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from store.models import Order
from ecommerce.settings import TIME_ZONE


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


def filter_orders(request):
    orders = Order.objects.exclude(status=False)
    
    transaction_id = request.GET.get('transaction_id')
    email = request.GET.get('email')
    date_ordered_min = request.GET.get('date_ordered_min')
    date_ordered_max = request.GET.get('date_ordered_max')
    status = request.GET.get('status')
    
    if is_valid_queryparam(transaction_id):
        orders = orders.filter(transaction_id__icontains=transaction_id)
        
    if is_valid_queryparam(email):
        orders = orders.filter(customer__email__icontains=email)
        
    if is_valid_queryparam(date_ordered_min):
        orders = orders.filter(date_ordered__gte=(date_ordered_min + ' 00:00:00.000000+00:00'))
        
    if is_valid_queryparam(date_ordered_max):
        orders = orders.filter(date_ordered__lte=(date_ordered_max + ' 23:59:59.999999+00:00'))
        
    if is_valid_queryparam(status):
        orders = orders.filter(status=status)
        
    sort_transaction_id = request.GET.get('sort_transaction_id')
    sort_email = request.GET.get('sort_email')
    sort_date_ordered = request.GET.get('sort_date_ordered')
    sort_status = request.GET.get('sort_status')
    
    if is_valid_sortparam(sort_transaction_id):
        if sort_transaction_id == '1':
            orders = orders.order_by('-transaction_id')
        elif sort_transaction_id == '2':
            orders = orders.order_by('transaction_id')
    
    if is_valid_sortparam(sort_email):
        if sort_email == '1':
            orders = orders.order_by('-customer')
        elif sort_email == '2':
            orders = orders.order_by('customer')
    
    if is_valid_sortparam(sort_date_ordered):
        if sort_date_ordered == '1':
            orders = orders.order_by('-date_ordered')
        elif sort_date_ordered == '2':
            orders = orders.order_by('date_ordered')
    
    if is_valid_sortparam(sort_status):
        if sort_status == '1':
            orders = orders.order_by('-status')
        elif sort_status == '2':
            orders = orders.order_by('status')
    
    page_orders = paginate_orders(request, orders)
    page = request.GET.get('page')
    number_of_displayed = 20

    if page:
        page = int(page)
        if page_orders.paginator.num_pages == 1:
            show_next_page = None
        elif page < page_orders.paginator.num_pages:
            show_next_page = True
        elif page >= page_orders.paginator.num_pages:
            show_next_page = False
            
        if page < page_orders.paginator.num_pages and show_next_page is not False:
            displayed_orders = number_of_displayed * int(page)
        else:
            displayed_orders = (number_of_displayed * int(page)) - ((page_orders.paginator.num_pages * number_of_displayed) - (page_orders.paginator.object_list.count()))
    else:
        show_next_page = None
        displayed_orders = page_orders.paginator.object_list.count()
        
    context = {
        'orders': page_orders,
    }
    
    return JsonResponse({
      'html': render_to_string('sales_dashboard/orders-list.html', context, request),
      'show_next_page': show_next_page,
      'displayed_orders': displayed_orders,
      'total_orders': page_orders.paginator.object_list.count()
    })
    

def paginate_orders(request, orders):
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_orders = paginator.get_page(page_number)
    return page_orders


def change_order_status(request, order):
    status = json.loads(request.body)['status']
    if status == '1' or status == '2' or status == '3':
        order.status = status
        order.save()
        date_updated = date(order.date_updated, 'm/d/Y G:i:s')
        
    return JsonResponse({'status': status, 'date_updated': date_updated}, safe=True)