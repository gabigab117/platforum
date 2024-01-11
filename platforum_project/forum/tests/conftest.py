import pytest

from forum.models import Theme


@pytest.fixture
def theme_1(db):
    return Theme.objects.create(name="dev")
