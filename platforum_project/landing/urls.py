from django.urls import path

from landing.views import index

app_name = "landing"
urlpatterns = [
    path('', index, name="index"),
]
