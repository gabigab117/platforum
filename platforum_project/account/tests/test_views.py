import pytest
from unittest.mock import patch
from django.urls import reverse
from account.models import CustomUser


def test_signup_view_get(client):
    url = reverse("account:signup")
    response = client.get(url)
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_signup_view_post(client):
#     url = reverse("account:signup")
#     response = client.post(url, {"username": "Patrick",
#                                  "email": "patrick.trouve5@sfr.fr",
#                                  "first_name": "Patrick",
#                                  "last_name": "Trouvé",
#                                  "password1": "Ringo_Star60456",
#                                  "password2": "Ringo_Star60456"})
#     user = CustomUser.objects.get(username="Patrick")


def test_signin_view_get(client):
    url = reverse("account:login")
    response = client.get(url)
    assert response.status_code == 200


def test_signin_view_post(client, user_1):
    url = reverse("account:login")
    response = client.post(url, {"username": "gab", "password": "12345678"})
    assert user_1.is_authenticated
    assert response["Location"] == reverse("landing:index")


def test_super_user(superuser_1):
    assert superuser_1.is_superuser
