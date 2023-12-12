from account.models import CustomUser

DEFAULT_ADMIN = CustomUser.objects.get(username="gabigab117")
