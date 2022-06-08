import pytest
from django.urls import reverse
from notes.models import Note

pytestmark = pytest.mark.django_db


@pytest.fixture
def authentication_user(client, django_user_model):
    user = django_user_model.objects.create_user(username='Ankit', password='7777')
    url = reverse('login')
    data = {'username': 'Ankit', 'password': '7777'}
    response = client.post(url, data)
    # headers = {
    #     "HTTP_AUTHORIZATION": "Bearer " + response.data["data"]["token"],
    #     "content-type": 'application/json',
    # }
    token = "Bearer " + response.data["data"]["token"]
    return token, user.id


class TestNoteAPI:
    """
        Test Login API
    """

    @pytest.mark.django_db
    def test_response_as_note_creation(self, client, django_user_model, authentication_user):

        token, user_id = authentication_user
        print(token, user_id)

        url = reverse('new_note')
        data = {'title': 'First Note', 'description': 'My first test note', 'user': user_id}
        response = client.post(url, data, content_type='application/json', HTTP_AUTHORIZATION=token)
        assert response.status_code == 201

    # @pytest.mark.django_db
    # def test_response_as_note_check(self, client, django_user_model):
    #     user = django_user_model.objects.create_user(username='Ankit', password='7777')
    #     url = reverse('login')
    #     data = {'username': 'Ankit', 'password': '7777'}
    #     response = client.post(url, data)
    #     assert response.status_code == 200
    #
    #     url = reverse('new_note')
    #     data = {'title': 'First Note', 'description': 'My first test note', 'user': user.id}
    #     response = client.post(url, data)
    #     assert response.status_code == 201
    #
    #     url = reverse('new_note')
    #     data = {'user': 1}
    #     response = client.get(url, data)
    #     assert response.status_code == 200
    #
    # @pytest.mark.django_db
    # def test_response_as_delete_note(self, client, django_user_model):
    #     user = django_user_model.objects.create_user(username='Ankit', password='7777')
    #     print(user.id)
    #     url = reverse('login')
    #     data = {'username': 'Ankit', 'password': '7777'}
    #     response = client.post(url, data)
    #     assert response.status_code == 200
    #
    #     # url = reverse('new_note')
    #     data = {'title': 'First Note', 'description': 'My first test note', 'user': user}
    #     # response = client.post(url, data)
    #     # assert response.status_code == 201
    #
    #     note = Note.objects.create(**data)
    #     url = reverse('note_id', kwargs={'pk': note.id})
    #     data = {'user': user.id}
    #     response = client.delete(url, data)
    #     assert response.data == {'message': 'Note deleted'}
    #     assert response.status_code == 204
