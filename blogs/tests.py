from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, PostDetailView
from .models import Post


# Create your tests here.
class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class PostObjectTests(TestCase):
    def setUp(self):
        Post.objects.create(title='Django', body='Django board.', image=None, created_by_id=1)

    def test_board_topics_view_success_status_code(self):
        url = reverse('blogs')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('blogs')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/blogs/1/')
        self.assertEquals(view.func, PostDetailView.render_to_response)
