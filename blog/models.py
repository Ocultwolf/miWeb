from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=160)
    title_en = models.CharField(max_length=160, blank=True)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=260)
    excerpt_en = models.CharField(max_length=320, blank=True)
    content = models.TextField()
    content_en = models.TextField(blank=True)
    cover_label = models.CharField(max_length=80, blank=True)
    cover_label_en = models.CharField(max_length=80, blank=True)
    published_at = models.DateTimeField()
    published = models.BooleanField(default=True)
    source_key = models.CharField(max_length=160, unique=True, null=True, blank=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
