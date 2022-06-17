import logging
import jwt
import redis
import json

from notes.models import Note
from notes.serializers import NoteSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.utils import verify_token
from .redis import RedisFunction

logger = logging.getLogger(__name__)


class NoteDetail(APIView):
    """
    Create, update and delete notes for specific user
    """

    @staticmethod
    def _get_object(pk):
        """
        Get the object of data from database using primary key
        """
        note_query = Note.objects.filter(pk=pk)
        try:
            return note_query.first()
        except note_query.DoesNotExist:
            raise Http404

    @verify_token
    def get(self, request, pk=None):
        """
        List of notes from database
        """
        try:
            user_id = request.data.get("user")
            notes = Note.objects.filter(user__id=user_id)
            serializer = NoteSerializer(notes, many=True)
            RedisFunction.set_key(user_id, json.dumps(serializer.data))
            data_fetch = RedisFunction.get_key(user_id)
            return Response({"data": json.loads(data_fetch)}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception('Data not found', e)
            print(e)
            return Response({'message': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)

    @verify_token
    def post(self, request):
        """
        Add a new note
        """
        try:
            user_id = request.data.get("user")
            serializer = NoteSerializer(data=request.data) # serialzer.data
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data_fetch = json.dumps(request.data)
            RedisFunction.set_key(user_id, data_fetch)
            data_fetch = RedisFunction.get_key(user_id)
            return Response({'data': json.loads(data_fetch)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception('Data entered not correct', e)
            print(e)
            return Response({'message': 'Data not found'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @verify_token
    def put(self, request):
        """
        Add some data in note
        """
        try:
            note = self._get_object(pk=request.data.get('id'))
            serializer = NoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': serializer.data, 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception('Data entered not correct', e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request, pk):
        """
        Delete a note using its primary key
        """
        try:
            note = self._get_object(pk)
            note.delete()
            return Response({'message': 'Note deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception('Data not able to delete', e)
            return Response(status=status.HTTP_404_NOT_FOUND)
