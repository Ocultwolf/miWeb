from django.urls import path
from .views import blog_index, blog_detail

urlpatterns = [
    path('', blog_index, name='blog_index'),
    path('<slug:slug>/', blog_detail, name='blog_detail'),
]
