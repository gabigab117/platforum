from django.urls import path
from .views import signup, LoginUser, logout_view, UserChangePassword, UserPasswordDone, UserResetPassword, \
    UserResetDone, UserResetConfirm, UserResetComplete, profile_view

app_name = "account"
urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('change-password/', UserChangePassword.as_view(), name="change-password"),
    path('password-done/', UserPasswordDone.as_view(), name="password-done"),
    path('password-reset/', UserResetPassword.as_view(), name="password-reset"),
    path('password-reset-done/', UserResetDone.as_view(), name="reset-done"),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', UserResetConfirm.as_view(), name="reset-confirm"),
    path('reset-complete/', UserResetComplete.as_view(), name="reset-complete"),
    path('profile/', profile_view, name="profile"),
]
