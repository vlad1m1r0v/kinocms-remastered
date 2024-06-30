from django.urls import path
from .consumers import MailingConsumer

ws_urlpatterns = [
    path('ws/<str:task_id>/', MailingConsumer.as_asgi()),
]
