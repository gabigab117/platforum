from django.urls import path
from .views import signup


app_name = "account"
urlpatterns = [
    path('signup/', signup, name="signup"),
]
