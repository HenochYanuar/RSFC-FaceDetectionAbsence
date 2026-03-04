from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active(context, *url_names):
    request = context['request']
    current_url = request.resolver_match.url_name

    if current_url in url_names:
        return "active"
    return ""


@register.simple_tag(takes_context=True)
def is_open(context, *url_names):
    request = context['request']
    current_url = request.resolver_match.url_name

    if current_url in url_names:
        return "menu-open"
    return ""