import logging
from notes.models import Note
from notes.serializers import NoteSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.utils import verify_token

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

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

    @swagger_auto_schema(operation_summary="Fetch notes")
    @verify_token
    def get(self, request, pk=None):
        """
        List of notes from database
        """
        # try:
        notes = Note.objects.filter(user__id=request.data.get("user"))
        serializer = NoteSerializer(notes, many=True)
        if pk:
            notes = notes.get(pk=pk)
            serializer = NoteSerializer(notes)
        logger.info(serializer.data)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        # except Exception as e:
        #     logger.exception('Data not found', e)
        #     # return Response({'message': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(operation_summary="New note",  request_body=NoteSerializer)
    @verify_token
    def post(self, request):
        """
        Add a new note
        """
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception('Data entered not correct', e)
            return Response({'message': 'Data not found'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @swagger_auto_schema(operation_summary="Update notes", request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="note_id"),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description")
            }
        ))
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

    @swagger_auto_schema(operation_summary="delete note", request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="note_id")}))
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
