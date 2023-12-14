from django.urls import path
from .views import create_forum, index

app_name = "forum"
urlpatterns = [
    path('create-forum/', create_forum, name="create-forum"),
    path('index/<str:slug>', index, name="index"),
]
