import pytest

import json

from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestLoginAPI:
    """

        Test Login API

    """

    @pytest.mark.django_db
    def test_response_as_login_successful(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Ankit', password='7777')
        url = reverse('login')
        # Login successful
        data = {'username': 'Ankit', 'password': '7777'}
        response = client.post(url, data)
        assert response.status_code == 200
        json_data = json.loads(response.content)
        assert json_data['data']['username'] == 'Ankit'

    @pytest.mark.django_db
    def test_response_as_login_failed(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Ankit', password='7777')
        url = reverse('registration')
        # Login failed
        data = {'username': 'Ankit', 'password': '1234'}
        response = client.post(url, data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_registration(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Ankit', password='7777')
        url = reverse('registration')
        # Login failed
        data = {'username': 'Ankit', 'password': '1234'}
        response = client.post(url, data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_validation(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Ankit', password='7777')
        url = reverse('login')
        # Validation error
        data = {'username': 'Ankit Ghosh', 'password': ''}
        response = client.post(url, data)
        assert response.status_code == 401
