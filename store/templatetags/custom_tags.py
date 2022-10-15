from django import template

register = template.Library()

@register.filter(name='email_username')
def email_username(value):
  return str(value).split('@')[0]