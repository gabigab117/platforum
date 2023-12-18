from django.urls import path
from .views import create_forum, index, sub_category_view

app_name = "forum"
urlpatterns = [
    path('create-forum/', create_forum, name="create-forum"),
    path('index/<str:slug>', index, name="index"),
    path('<str:slug_forum>/sub-category/<int:pk>/<str:slug_sub_category>', sub_category_view, name="sub-category"),
]
