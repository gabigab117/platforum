import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertContains, assertNotContains

from forum.default_data.messages import welcome_message
from forum.models import Forum, Theme, ForumAccount, Category, SubCategory, Topic, Message


@pytest.mark.django_db
def test_create_forum_view_post(client: Client, theme_1, user_1):
    # Given an user wants to create a forum
    client.login(username=user_1.username, password="12345678")
    # When user validates the form
    response = client.post(reverse("forum:create-forum"), data={"name": "devforum",
                                                                "theme": theme_1.id,
                                                                "description": "Forum des devs",
                                                                "thumbnail": ""})
    # Then a Forum is created with default data
    forum = Forum.objects.get(name="devforum")
    account: ForumAccount = ForumAccount.objects.get(forum=forum)
    category = Category.objects.get(name="Catégorie Test", forum=forum)
    sub_category = SubCategory.objects.get(name="Sous catégorie Test", category=category)
    topic = Topic.objects.get(title="Bienvenu(e)", sub_category=sub_category, account=account)
    message = Message.objects.get(account=account, topic=topic, message=welcome_message(account))
    assert forum.name == "devforum"
    assert account.user == user_1
    assert account.forum_master
    assert category.forum == forum
    assert sub_category.category == category
    assert topic.account == account
    assert "Ton forum est crée" in message.message
    assert response.status_code == 302
    assertRedirects(response, reverse("forum:index", args=["devforum", 1]))


@pytest.mark.django_db
def test_signup_post(client: Client, forum_1, user_3):
    # Given an user wants to create an account
    client.login(username=user_3.username, password="12345678")
    data = {"thumbnail": ""}
    # When user validates the form
    response = client.post(reverse("forum:signup", args=["metal", 1]), data=data)
    # Then redirect to forum index, user's not the forum_master and is active
    assertRedirects(response, reverse("forum:profile", args=["metal", 1]))
    account: ForumAccount = ForumAccount.objects.get(forum=forum_1, user=user_3)
    assert account.user.username == "ely"
    assert not account.forum_master
    assert account.active
    assert account.forum.name == "Metal"


def test_index_forum_view_if_no_account_platforum(client: Client, forum_1):
    # Given no user so... no login
    # When the visitor get forum index
    response = client.get(reverse("forum:index", args=["metal", 1]))
    forum = Forum.objects.get(pk=1)
    # Then visitor is redirects to login view
    assert forum.name == "Metal"
    assert response.status_code == 302
    assertRedirects(response, f"{reverse("account:login")}?next={reverse("forum:index", args=["metal", 1])}")


def test_index_forum_view_if_platforum_account_but_no_forum_account(client: Client, forum_1, user_3):
    # Given an user but no forum account
    client.login(username=user_3.username, password="12345678")
    assert user_3.username == "ely"
    # When user gets forum index
    response = client.get(reverse("forum:index", args=["metal", 1]))
    forum = Forum.objects.get(pk=1)
    # Then the navbar has just Devenir membre de ce forum
    assert forum.name == "Metal"
    assert response.status_code == 200
    assertContains(response, "Devenir membre de ce forum")
    assertNotContains(response, "Profil")
    assertNotContains(response, "Messagerie privée")
    assertNotContains(response, "Liste des membres")


def test_index_forum_view_if_platforum_account_and_forum_account(client: Client, forum_1, user_2, forum_account_1):
    # Given an user with a forum account
    client.login(username=user_2.username, password="12345678")
    assert user_2.username == "pat"
    # When user gets forum index
    response = client.get(reverse("forum:index", args=["metal", 1]))
    print(user_2.retrieve_forum_account(forum_1))
    forum = Forum.objects.get(pk=1)
    # Then the navbar contains the items below (but not Devenir membre...)
    assert forum.name == "Metal"
    assert response.status_code == 200
    assertNotContains(response, "Devenir membre de ce forum")
    assertContains(response, "Profil")
    assertContains(response, "Messagerie privée")
    assertContains(response, "Liste des membres")
