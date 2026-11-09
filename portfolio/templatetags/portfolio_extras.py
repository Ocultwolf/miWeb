from django import template

from blog.models import Post

register = template.Library()


@register.simple_tag
def latest_posts(n=4):
    """Últimos posts publicados, para enseñar el blog en la home sin tocar la vista."""
    return Post.objects.filter(published=True)[:n]


@register.simple_tag
def published_posts_count():
    return Post.objects.filter(published=True).count()
