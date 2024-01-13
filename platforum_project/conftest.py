import pytest
from account.models import CustomUser


@pytest.fixture()
def user_1(db):
    return CustomUser.objects.create_user(username="gab", email="g@g.com", first_name="Trouvé", last_name="Gabriel",
                                          password="12345678")


@pytest.fixture()
def user_2(db):
    return CustomUser.objects.create_user(username="pat", email="p@p.com", first_name="Trouvé", last_name="Patrick",
                                          password="12345678")


@pytest.fixture()
def user_3(db):
    return CustomUser.objects.create_user(username="ely", email="p@p.com", first_name="Trouvé", last_name="Ely",
                                          password="12345678")


@pytest.fixture()
def superuser_1(db):
    return CustomUser.objects.create_superuser(username="ely", email="e@e.com", first_name="Trouvé", last_name="Ely",
                                               password="12345678")
