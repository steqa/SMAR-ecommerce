from django import template

register = template.Library()

@register.filter
def allowed_users(user, allowed_roles=[]):
    if user.groups.exists():
        for group in user.groups.all():
            if group.name in allowed_roles:
                return True
        
        return False