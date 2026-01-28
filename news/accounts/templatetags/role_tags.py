from django import template

register = template.Library()

@register.filter
def has_role(user, role_name):
    if not user.is_authenticated:
        return False
    
    try:
        return user.profile.role.title.lower() == role_name.lower()
    except AttributeError:
        return False

@register.filter
def has_any_role(user, role_names):
    if not user.is_authenticated:
        return False
    
    try:
        user_role = user.profile.role.title.lower()
        roles = [role.strip().lower() for role in role_names.split(',')]
        return user_role in roles
    except AttributeError:
        return False