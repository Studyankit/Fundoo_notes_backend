import pytest

import json

from django.urls import reverse

pytestmark = pytest.mark.django_db


# class TestLoginAPI:
#     """
#
#         Test Login API
#
#     """
#
#     @pytest.mark.django_db
#     def test_response_as_login_succssful(self, client, django_user_model):
#         # Create user
#
#         user = django_user_model.objects.create_user(username='Minu', password='7777')
#
#         user.save()
#
#         url = reverse('auth_app:user_login')
#
#         # Login successful
#
#         data = {'username': 'Minu', 'password': '7777'}
#
#         response = client.post(url, data)
#
#         assert response.status_code == 200
#
#         json_data = json.loads(response.content)
#
#         assert json_data['data']['username'] == 'Minu'
#
#     @pytest.mark.django_db
#     def test_response_as_login_failed(self, client, django_user_model):
#         # Create user
#
#         user = django_user_model.objects.create_user(username='Minu', password='7777')
#
#         user.save()
#
#         url = reverse('auth_app:user_login')
#
#         # Login failed
#
#         data = {'username': 'Minu', 'password': '1234'}
#
#         response = client.post(url, data)
#
#         assert response.status_code == 400
