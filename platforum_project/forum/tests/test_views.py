import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertContains, assertNotContains

from forum.default_data.messages import welcome_message
from forum.models import Forum, Theme, ForumAccount, Category, SubCategory, Topic, Message


@pytest.mark.django_db
def test_create_forum_view_post(client: Client, theme_1, user_1, badges):
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
    assertRedirects(response, reverse("forum:index", args=[forum.slug, forum.pk]))


@pytest.mark.django_db
def test_signup_post(client: Client, forum_1, user_3):
    # Given an user wants to create an account
    client.login(username=user_3.username, password="12345678")
    data = {"thumbnail": ""}
    # When user validates the form
    response = client.post(reverse("forum:signup", args=[forum_1.slug, forum_1.pk]), data=data)
    # Then redirect to forum index, user's not the forum_master and is active
    assertRedirects(response, reverse("forum:profile", args=[forum_1.slug, forum_1.pk]))
    account: ForumAccount = ForumAccount.objects.get(forum=forum_1, user=user_3)
    assert account.user.username == "ely"
    assert not account.forum_master
    assert account.active
    assert account.forum.name == "Metal"


def test_index_forum_view_if_no_account_platforum(client: Client, forum_1):
    # Given no user so... no login
    # When the visitor get forum index
    response = client.get(reverse("forum:index", args=[forum_1.slug, forum_1.pk]))
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
    response = client.get(reverse("forum:index", args=[forum_1.slug, forum_1.pk]))
    forum = Forum.objects.get(pk=1)
    # Then the navbar has just Devenir membre de ce forum
    assert forum.name == "Metal"
    assert response.status_code == 200
    assertContains(response, "Devenir membre de ce forum")
    assertNotContains(response, "Profil")
    assertNotContains(response, "Messagerie privée")
    assertNotContains(response, "Liste des membres")


def test_index_forum_view_if_platforum_account_and_forum_account(client: Client, forum_1, user_2, forum_account_1,
                                                                 badges):
    # Given an user with a forum account
    client.login(username=user_2.username, password="12345678")
    assert user_2.username == "pat"
    # When user gets forum index
    response = client.get(reverse("forum:index", args=[forum_1.slug, forum_1.pk]))
    forum = Forum.objects.get(pk=1)
    # Then the navbar contains the items below (but not Devenir membre...)
    assert forum.name == "Metal"
    assert response.status_code == 200
    assertNotContains(response, "Devenir membre de ce forum")
    assertContains(response, "Profil")
    assertContains(response, "Messagerie privée")
    assertContains(response, "Liste des membres")


def test_index_admin_view_if_not_forum_master_account(client: Client, forum_1, forum_account_1, user_2):
    # Given an user with no forum master status
    client.force_login(user_2)
    # When user gets admin index
    response = client.get(reverse("forum:admin-index", args=[forum_1.slug, forum_1.pk]))
    # Permission Denied !
    assert response.status_code == 403


def test_index_admin_view_if_forum_master(client: Client, forum_1, user_1, forum_master_account_1):
    # Given an user with forum master status
    client.force_login(user_1)
    # When user gets admin index
    response = client.get(reverse("forum:admin-index", args=[forum_1.slug, forum_1.pk]))
    # It's... ok ! :)
    assert response.status_code == 200


def test_pin_topic_if_not_forum_master_account(client: Client, forum_1, forum_account_1, user_2, topic_1):
    # Given an user with no forum master status
    client.force_login(user_2)
    # When post to pin or unpic topic
    response = client.post(reverse("forum:pin", args=[forum_1.pk, topic_1.pk]))
    # hello 403 !
    topic_1.refresh_from_db()
    assert response.status_code == 403
    assert topic_1.pin is False


def test_pin_topic_if_forum_master(client: Client, forum_1, user_1, forum_master_account_1, topic_1: Topic):
    # Given the forum master
    client.force_login(user_1)
    # When post to pin or unpin topic
    response = client.post(reverse("forum:pin", args=[forum_1.pk, topic_1.pk]))
    # response 302
    topic_1.refresh_from_db()
    assert response.status_code == 302
    assert topic_1.pin is True
