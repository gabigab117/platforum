from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField

from platforum_project.settings import TEST_MODE


class SignUpForm(UserCreationForm):
    if not TEST_MODE:
        security = ReCaptchaField(label="Sécurité")

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "last_name", "first_name"]
