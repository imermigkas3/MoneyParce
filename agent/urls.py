from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat, name='agent.chat'),
    path('chat/send-message/',views.send_message, name='send_message')
]