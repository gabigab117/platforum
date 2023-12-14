from django.urls import path
from .views import create_forum

app_name = "forum"
urlpatterns = [
    path('create-forum/', create_forum, name="create-forum"),

]
