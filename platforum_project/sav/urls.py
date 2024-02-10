from django.urls import path
from .views import contact_view, legal_view


app_name = "sav"
urlpatterns = [
    path('contact/', contact_view, name="contact"),
    path('legal/', legal_view, name="legal")
    ]
