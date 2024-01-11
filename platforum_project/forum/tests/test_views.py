import pytest
from django.test import Client
from django.urls import reverse

from forum.models import Forum, Theme


@pytest.mark.django_db
def test_create_forum_view_post(client: Client, theme_1, user_1):
    client.login(username=user_1.username, password="12345678")
    response = client.post(reverse("forum:create-forum"), data={"name": "devforum",
                                                                "theme": theme_1,
                                                                "description": "Forum des devs"})

