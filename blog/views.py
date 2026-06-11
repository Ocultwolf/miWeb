from django.shortcuts import get_object_or_404, render
from .models import Post


def blog_index(request):
    posts = Post.objects.filter(published=True)
    return render(request, 'blog/index.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    return render(request, 'blog/detail.html', {'post': post})
