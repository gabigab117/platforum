import pytest
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from pytest_django.asserts import assertRedirects
from django.urls import reverse

from account.models import CustomUser
from account.verification import email_verification_token


def test_signup_view_get(client):
    url = reverse("account:signup")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_view_post(client, mailoutbox):
    url = reverse("account:signup")
    response = client.post(url, {"username": "Patrick",
                                 "email": "patrick.trouve5@sfr.fr",
                                 "first_name": "Patrick",
                                 "last_name": "Trouvé",
                                 "password1": "Ringo_Star60456",
                                 "password2": "Ringo_Star60456"})
    user = CustomUser.objects.get(username="Patrick")
    assert not user.is_active
    assertRedirects(response, reverse("landing:index"))
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == 'Activation du compte PlatForum'


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


@pytest.mark.django_db
def test_account_activation(client):
    user = CustomUser.objects.create_user(username="roro", email="r@p.com", first_name="r", last_name="r",
                                          password="12345678")
    user.is_active = False
    user.save()

    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)

    url = reverse('account:activate', args=[uidb64, token])
    response = client.get(url)
    user.refresh_from_db()
    assert user.is_active
    assert response.status_code == 302
    assertRedirects(response, reverse("landing:index"))
