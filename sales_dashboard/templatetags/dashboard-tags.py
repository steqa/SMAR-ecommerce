from django import template

register = template.Library()


@register.filter
def get_orders_by_status(queryset, status=''):
    queryset = queryset.filter(status=int(status))
    return queryset


@register.filter
def get_month_name_by_number(number):
    months = {'1': 'Янв',
              '2': 'Фев',
              '3': 'Мар',
              '4': 'Апр',
              '5': 'Май',
              '6': 'Июн',
              '7': 'Июл',
              '8': 'Авг',
              '9': 'Сен',
              '10': 'Окт',
              '11': 'Ноя',
              '12': 'Дек'}
    
    return months[str(number)]