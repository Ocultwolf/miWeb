from django.shortcuts import render
from .models import Project


def home(request):
    projects = Project.objects.all()[:6]
    featured = Project.objects.filter(featured=True)[:3]
    return render(request, 'portfolio/home.html', {
        'projects': projects,
        'featured': featured,
    })
