from django.urls import path, include
from . import views

urlpatterns = [
    path('notes/<int:pk>/', views.NoteDetail.as_view(), name='note_id'),
    path('notes/', views.NoteDetail.as_view(), name='new_note')
]