from django.urls import path
from . import views

urlpatterns = [
    path('home', views.raw_query, name='get'),
    path('note_home', views.NoteQuery.as_view()),
    path('note_home/<int:pk>', views.NoteQuery.as_view())
]