from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "last_name", "first_name"]
