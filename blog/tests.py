from django.test import TestCase
from django.urls import reverse

from .models import Post


class BlogViewsTests(TestCase):
    def test_blog_index_and_detail_render(self):
        post = Post.objects.filter(published=True).first()
        self.assertIsNotNone(post)

        index_response = self.client.get(reverse("blog_index"))
        self.assertEqual(index_response.status_code, 200)
        self.assertContains(index_response, "Blog")

        detail_response = self.client.get(reverse("blog_detail", args=[post.slug]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, post.title)
