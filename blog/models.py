from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=260)
    content = models.TextField()
    cover_label = models.CharField(max_length=80, blank=True)
    published_at = models.DateTimeField()
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
