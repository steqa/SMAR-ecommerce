import json
from django.http.response import JsonResponse
from django.template.defaultfilters import date
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.shortcuts import render
from store.models import Order
from .utils import is_valid_queryparam, is_valid_sortparam, get_orders_by_period, get_chart_data
from authentication.decorators import allowed_users


@allowed_users(allowed_roles=['seller'])
def dashboard(request):
    orders = Order.objects.exclude(status=False)
    orders_by_year = get_orders_by_period('year')['orders_by_period']
    orders_by_all_years = get_orders_by_period('all_years')['orders_by_period']

    context = {
        'orders': orders,
        'orders_by_year': orders_by_year,
        'orders_by_all_years': orders_by_all_years,
    }
    return render(request, 'sales_dashboard/dashboard.html', context)


def render_chart_data(request):
    period = 'all_years'
    sales_chart_data = get_chart_data(datatype='sales', period=period, year=2022, month=10)
    revenue_chart_data = get_chart_data(datatype='revenue', period=period, year=2022, month=10)

    context = {}
    return JsonResponse({
      'html': render_to_string('sales_dashboard/charts.html', context, request),
      'period': period,
      'sales_chart_data': sales_chart_data,
      'revenue_chart_data': revenue_chart_data,
    })


@allowed_users(allowed_roles=['seller'])
def orders(request):
    orders = Order.objects.exclude(status=False)
    page_orders = paginate_orders(request, orders)
    
    if page_orders.paginator.num_pages == 1:
        displayed_orders = page_orders.paginator.object_list.count()
    else:
        displayed_orders = 20
    
    context = {
        'orders': page_orders,
        'displayed_orders': displayed_orders,
        'total_orders': page_orders.paginator.object_list.count()
    }
    return render(request, 'sales_dashboard/orders.html', context)

@allowed_users(allowed_roles=['seller'])
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    order_items = order.orderitem_set.all()
    shipping_address = order.shippingaddress_set.get()
    if request.method == 'POST':
        status = json.loads(request.body)['status']
        if status == '1' or status == '2' or status == '3':
            order.status = status
            order.save()
            date_updated = date(order.date_updated, 'm/d/Y G:i:s')
            
        return JsonResponse({'status': status, 'date_updated': date_updated}, safe=True)
    
    context = {
        'order': order,
        'order_items': order_items,
        'shipping_address': shipping_address,
    }
    return render(request, 'sales_dashboard/order-detail.html', context)


def orders_filter(request):
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