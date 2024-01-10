from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField


class SignUpForm(UserCreationForm):
    security = ReCaptchaField(label="Sécurité")

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "last_name", "first_name", "security"]
