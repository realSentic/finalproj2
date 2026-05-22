from django import template

register = template.Library()

@register.filter
def short_currency(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value

    if value >= 1_000_000_000_000:
        return f"₱{value / 1_000_000_000_000:.1f}T".replace(".0T", "T")
    elif value >= 1_000_000_000:
        return f"₱{value / 1_000_000_000:.1f}B".replace(".0B", "B")
    elif value >= 1_000_000:
        return f"₱{value / 1_000_000:.1f}M".replace(".0M", "M")
    elif value >= 1_000:
        return f"₱{value / 1_000:.1f}K".replace(".0K", "K")
    else:
        return f"₱{value:.0f}"