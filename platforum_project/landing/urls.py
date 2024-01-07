from django.urls import path

from landing.views import index, forums_list_view

app_name = "landing"
urlpatterns = [
    path('', index, name="index"),
    path('forums-list/', forums_list_view, name="forums-list")
]
