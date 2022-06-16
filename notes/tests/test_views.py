import pytest
from django.urls import reverse
from rest_framework.utils import json

from notes.models import Note
from user.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def authentication_user(client, django_user_model):
    user = django_user_model.objects.create_user(username='Ankit', password='7777')
    url = reverse('login')
    data = {'username': 'Ankit', 'password': '7777'}
    response = client.post(url, data)
    token = "Bearer " + response.data["data"]["token"]
    return token, user.id


class TestNoteAPI:
    """
        Test Login API
    """

    @pytest.mark.django_db
    def test_response_as_note_creation(self, client, django_user_model, authentication_user):
        token, user_id = authentication_user

        url = reverse('new_note')
        data = {'title': 'First Note', 'description': 'My first test note', 'user': user_id}
        response = client.post(url, data, content_type='application/json', HTTP_AUTHORIZATION=token)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_response_as_note_check(self, client, authentication_user):
        token, user_id = authentication_user

        url = reverse('new_note')
        data = {'title': 'First Note', 'description': 'My first test note', 'user': user_id}
        response = client.post(url, data, content_type='application/json', HTTP_AUTHORIZATION=token)
        assert response.status_code == 201

        url = reverse('new_note')
        data = {'HTTP_TOKEN': token}
        response = client.get(url, data, content_type='application/json', HTTP_AUTHORIZATION=token)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_response_as_update_notes(self, client, authentication_user):
        token, user_id = authentication_user

        # new note
        url = reverse('new_note')
        data = {'title': 'First Note', 'description': 'My first test note', 'user': user_id}
        header = {'content_type': 'application/json', "HTTP_AUTHORIZATION": token}
        response = client.post(url, data, **header)
        assert response.status_code == 201

        # Update notes
        url = reverse('new_note')
        data = {'user': user_id, 'title': 'first note change', 'description': 'First note data changed'}
        header = {'content_type': 'application/json', "HTTP_AUTHORIZATION": token}
        response = client.put(url, data, **header)
        json_data = json.loads(response.content)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_response_as_delete_notes(self, client, authentication_user):
        token, user_id = authentication_user
        user = User.objects.get(pk=user_id)

        # new note
        data = {'title': 'First Note', 'description': 'My first test note', 'user': user}
        note = Note.objects.create(**data)
        # data["user"] = user_id
        # url = reverse('new_note')
        # response = client.post(url, data, content_type='application/json', HTTP_AUTHORIZATION=token)
        # print(response.data["data"]["id"], "data check ")
        # assert response.status_code == 201

        # Delete notes
        url = reverse('note_id', kwargs={'pk': note.id})
        response = client.delete(url, HTTP_AUTHORIZATION=token)
        assert response.status_code == 204
