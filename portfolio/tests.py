from django.test import TestCase
from django.urls import reverse

from .models import Project


class PortfolioViewsTests(TestCase):
    def test_home_page_shows_projects_and_blog_preview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Proyectos")
        self.assertContains(response, "Blog")
        self.assertTrue(Project.objects.filter(featured=True).exists())
