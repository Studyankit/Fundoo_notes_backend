from rest_framework import serializers
from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    Note Serializer
    """
    class Meta:
        model = Note
        fields = ['user', 'description', 'title', 'id']
