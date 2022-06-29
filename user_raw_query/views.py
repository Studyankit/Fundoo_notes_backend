import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.models import Note
from notes.serializers import NoteSerializer
from user.models import User
from user.serializers import UserSerializer
from user.utils import verify_token
from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))for row in cursor.fetchall()]


@api_view(['GET'])
def raw_query(request):
    if request.method == 'GET':
        data = User.objects.raw('SELECT * from user_user WHERE id = %s ', [39])
        serializer = UserSerializer(data, many=True)
        dict_data = json.dumps(serializer.data)
        print(dict_data)
        return Response({
            'message': serializer.data[0]
        })


class NoteQuery(APIView):

    # @verify_token
    def get(self, request):
        data = Note.objects.raw('Select * from notes_note')
        serializer = NoteSerializer(data, many=True)
        return Response({
            'message': serializer.data
        })

    def post(self, request):
        with connection.cursor() as cursor:
            data = cursor.execute("Insert into notes_note (title, description, user_id) VALUES (%s,%s,%s)",
                                  (request.data['title'],
                                   request.data['description'],
                                   request.data['user']))
            print(data)
            cursor.execute("SELECT * FROM notes_note")
            row = dictfetchall(cursor)
            print(row)

        return Response({
            'message': row
        })

    def delete(self, request, pk):
        with connection.cursor() as cursor:
            cursor.execute('delete from notes_note where id=%s', [pk])
            row = dictfetchall(cursor)
            return Response({
                "message": "user deleted successfully"
            })

    def put(self, request):
        with connection.cursor() as cursor:
            cursor.execute("update notes_note set title=%s,description=%s where id=%s",
                           [request.data.get('title'),
                            request.data.get('description'),
                            request.data.get('id')])

            return Response({
                "message": "user update successfully"
            })
