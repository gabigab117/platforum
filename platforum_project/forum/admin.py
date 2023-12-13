from django.contrib import admin
from .models import Forum, ForumAccount, Category, Topic, Message, PersonalMessaging


admin.site.register(Forum)
admin.site.register(ForumAccount)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(PersonalMessaging)
