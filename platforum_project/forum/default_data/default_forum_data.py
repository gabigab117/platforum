from forum.models import ForumAccount, Category, SubCategory, Topic, Message


def create_forum_with_data(form, user):
    form.instance.forum_master = user
    forum = form.save()
    ForumAccount.objects.create(forum=forum, user=user)
    category = Category.create_test_category(forum)
    sub_category = SubCategory.create_test_subcategory(category)
    topic = Topic.create_topic_test(sub_category, user)
    Message.message_test(topic, user)
