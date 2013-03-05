from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from .views import suscribe_newsletter


class SubscribeTestCase(TestCase):
    def test_an_anonymous_user_can_subscribe(self):
        data = {
            'email_user': 'edgar@poe.com',
        }

        request = RequestFactory().post('/', data)
        request.user = AnonymousUser()
        response = suscribe_newsletter(request)

        self.assertEqual(response.status_code, 200)
