from io import BytesIO
import pathlib
from platforum_project.settings import BASE_DIR

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from forum.models import Theme, Forum, ForumAccount, Category, SubCategory, Topic, Message, Badge


def create_test_image():
    image = Image.new('RGB', (100, 100), color='white')

    image_file = BytesIO()
    image.save(image_file, format="JPEG")
    image_file.seek(0)

    file_name = 'test_image.jpg'
    uploaded_image = SimpleUploadedFile(name=file_name, content=image_file.getvalue(), content_type='image/jpeg')
    return uploaded_image


@pytest.fixture
def theme_1(db):
    return Theme.objects.create(name="dev")


@pytest.fixture
def forum_1(db, user_1, theme_1):
    return Forum.objects.create(forum_master=user_1, name="Metal", theme=theme_1, description="Le forum du metal")


@pytest.fixture
def forum_master_account_1(db, forum_1, user_1):
    return ForumAccount.objects.create(forum=forum_1, user=user_1, forum_master=True)


@pytest.fixture
def forum_account_1(db, forum_1, user_2):
    return ForumAccount.objects.create(forum=forum_1, user=user_2)


@pytest.fixture
def category_1(db, forum_1):
    return Category.objects.create(name="Catégorie1", forum=forum_1)


@pytest.fixture
def sub_category_1(db, category_1):
    return SubCategory.objects.create(name="SousCatégorie1", category=category_1)


@pytest.fixture
def topic_1(db, sub_category_1, forum_master_account_1):
    return Topic.objects.create(title="Titre1", sub_category=sub_category_1, account=forum_master_account_1)


@pytest.fixture
def message_1(db, forum_master_account_1, topic_1):
    return Message.objects.create(message="message1", account=forum_master_account_1, topic=topic_1)


@pytest.fixture
def badges(db):
    description = ["Noo Badge", "100 messages", "50 messages", "10 messages", "Nouveau", "100 likes", "50 likes",
                   "10 likes", "Forum Master"]
    for el in description:
        Badge.objects.create(description=el, thumbnail=create_test_image())
    yield Badge.objects.all()
    path = BASE_DIR / "mediafiles"
    for file in path.rglob("test_image*"):
        file.unlink()
