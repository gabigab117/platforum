from django.urls import path
from .views import create_forum, index, sub_category_view, add_topic

app_name = "forum"
urlpatterns = [
    path('create-forum/', create_forum, name="create-forum"),
    path('<str:slug>/index/', index, name="index"),
    path('<str:slug_forum>/sub-category/<int:pk>/<str:slug_sub_category>', sub_category_view, name="sub-category"),
    path('<str:slug_forum>/<int:pk>/<str:slug_sub_category>/add/', add_topic, name="add-topic")
]
