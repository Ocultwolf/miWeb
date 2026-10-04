import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdownify(text):
    """Renderiza el contenido de un post (Markdown) a HTML. Los posts los escribimos nosotros, no los visitantes."""
    return mark_safe(md.markdown(text or "", extensions=["fenced_code", "tables", "sane_lists"]))
