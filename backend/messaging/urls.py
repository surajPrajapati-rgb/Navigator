
from django.urls import path
from . import views
# from .views import ChatHistoryView

urlpatterns = [
    path('create/', views.create_message, name='create_message'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('received/', views.received_messages, name='received_messages'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('chat_users/', views.chat_users, name='chat_users'),
    path('chat/<str:username>/', views.chat_history, name='chat_history'),
]