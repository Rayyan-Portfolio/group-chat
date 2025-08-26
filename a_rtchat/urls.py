from django.urls import path
from .views import *

urlpatterns = [
    path('', chat_group, name='home'),
]
