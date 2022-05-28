import logging

from notes.models import Note
from notes.serializers import NoteSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class NoteList(APIView):
    """
    List all Notes, or create a new Note.
    """

    def get(self, request, pk=None):
        try:
            Notes = Note.objects.filter(user__id=request.data.get('user'))
            serializer = NoteSerializer(Notes, data=request.data)
            logging.info(request.data)
            return Response(serializer.data, status=200)

        except Exception as e:
            logging.exception('Data not found', e)
            return Response(status=404)

    def post(self, request):
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            logging.exception('Data entered not correct', e)
            return Response(status=404)


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

    def get(self, request, pk=None):
        """
        List of notes from database
        """
        try:
            Notes = self._get_object(pk=pk)
            # Notes = Note.objects.filter(pk=pk)
            serializer = NoteSerializer(Notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            logging.info(request.data)
            return Response(serializer.data, status=200)

        except Exception as e:
            logging.exception('Data not found', e)
            return Response(status=404)

    def post(self, request, pk=None):
        """
        Add a new note
        """
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
        except Exception as e:
            logging.exception('Data entered not correct', e)
            return Response(status=404)

    def put(self, request, pk):
        """
        Add some data in note
        """
        try:
            note = self._get_object(pk)
            serializer = NoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
        except Exception as e:
            logging.exception('Data entered not correct', e)
            return Response(status=404)

    def delete(self, request, pk):
        """
        Delete a note using its primary key
        """
        try:
            note = self._get_object(pk)
            note.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.exception('Data not able to delete', e)
            return Response(status=404)
