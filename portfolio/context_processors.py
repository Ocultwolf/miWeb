from blog.models import Post


def blog_posts(request):
    return {'blog_posts': Post.objects.filter(published=True)[:3]}
