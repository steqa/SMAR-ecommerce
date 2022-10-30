from django import template

register = template.Library()

@register.filter
def get_orders_by_status(queryset, status=''):
    queryset = queryset.filter(status=int(status))
    return queryset