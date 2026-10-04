from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=120)
    title_en = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=220)
    short_description_en = models.CharField(max_length=220, blank=True)
    description = models.TextField()
    description_en = models.TextField(blank=True)
    technologies = models.CharField(max_length=220)
    link = models.URLField(blank=True)
    impact = models.CharField(max_length=160, blank=True)
    impact_en = models.CharField(max_length=160, blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
