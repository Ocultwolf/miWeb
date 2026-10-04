from django import template
from django.utils import translation

register = template.Library()


@register.filter
def localized(obj, field):
    """{{ post|localized:"title" }} -> post.title_en en inglés si existe; si no, el campo original
    (en español). Así una traducción que falta nunca deja un hueco en la página."""
    if translation.get_language() == "en":
        value = getattr(obj, f"{field}_en", "")
        if value:
            return value
    return getattr(obj, field, "")
