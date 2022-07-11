from rest_framework import serializers
from notes.models import Note, Label


class NoteSerializer(serializers.ModelSerializer):
    """
    Note Serializer
    """

    class Meta:
        model = Note
        fields = ['user', 'description', 'title', 'id']


class ShareNoteSerializer(serializers.ModelSerializer):
    """
    Note Serializer
    """

    class Meta:
        model = Note
        fields = ['user', 'id', 'collaborator']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['user', 'name', 'color', 'note']
