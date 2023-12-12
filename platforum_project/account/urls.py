from django.urls import path
from .views import signup, LoginUser, logout_view


app_name = "account"
urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
]
