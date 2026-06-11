from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'order', 'link')
    list_filter = ('featured',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description', 'technologies')
