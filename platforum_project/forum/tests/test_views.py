import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from forum.default_data.messages import welcome_message
from forum.models import Forum, Theme, ForumAccount, Category, SubCategory, Topic, Message


@pytest.mark.django_db
def test_create_forum_view_post(client: Client, theme_1, user_1):
    client.login(username=user_1.username, password="12345678")
    response = client.post(reverse("forum:create-forum"), data={"name": "devforum",
                                                                "theme": theme_1.id,
                                                                "description": "Forum des devs",
                                                                "thumbnail": ""})

    forum = Forum.objects.get(name="devforum")
    account = ForumAccount.objects.get(forum=forum)
    category = Category.objects.get(name="Catégorie Test", forum=forum)
    sub_category = SubCategory.objects.get(name="Sous catégorie Test", category=category)
    topic = Topic.objects.get(title="Bienvenu(e)", sub_category=sub_category, account=account)
    message = Message.objects.get(account=account, topic=topic, message=welcome_message(account))
    assert forum.name == "devforum"
    assert account.user == user_1
    assert category.forum == forum
    assert sub_category.category == category
    assert topic.account == account
    assert "Ton forum est crée" in message.message
    assert response.status_code == 302
    assertRedirects(response, reverse("forum:index", args=["devforum", 1]))
