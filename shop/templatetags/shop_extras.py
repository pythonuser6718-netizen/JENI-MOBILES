from django import template

register = template.Library()


@register.filter
def inr(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value
    s = f"{value:,.0f}"
    return f"₹{s}"


@register.filter
def times(number):
    try:
        return range(int(number))
    except (TypeError, ValueError):
        return range(0)
