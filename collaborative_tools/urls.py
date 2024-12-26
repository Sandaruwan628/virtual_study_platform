from django.urls import path
from . import views

urlpatterns = [
    path('whiteboard/<int:board_id>/', views.whiteboard, name='whiteboard'),
    path('whiteboards/', views.list_whiteboards, name='list_whiteboards'),
    path('whiteboards/create/', views.create_whiteboard, name='create_whiteboard'),
]
