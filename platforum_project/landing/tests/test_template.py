from django.test import Client
import pytest
from pytest_django.asserts import assertContains, assertNotContains
from django.urls import reverse


def test_if_administration_link_with_admin_user(client: Client, superuser_1):
    client.force_login(superuser_1)
    response = client.get(reverse("landing:index"))
    assertContains(response, "Administration")


def test_if_administration_link_with_user(client: Client, user_1):
    client.force_login(user_1)
    response = client.get(reverse("landing:index"))
    assertNotContains(response, "Administration")
