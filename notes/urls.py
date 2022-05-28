from django.urls import path, include
from . import views

urlpatterns = [
    path('notes/<int:pk>/', views.NoteDetail.as_view())
]