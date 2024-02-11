from django.contrib import admin
from .models import Forum, ForumAccount, Category, Topic, Message, Conversation, SubCategory, Notification, Badge, Like, \
    Theme

admin.site.register(Forum)
admin.site.register(ForumAccount)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(SubCategory)
admin.site.register(Notification)
admin.site.register(Badge)
admin.site.register(Like)
admin.site.register(Theme)
