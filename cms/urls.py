from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('addUser/', addUser, name='addUser'),
    # path('postUser/', addUser, name='postUser'),
]