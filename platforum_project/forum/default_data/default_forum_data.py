from forum.models import ForumAccount, Category, SubCategory, Topic, Message


def create_forum_with_data(form, user):
    forum = form.save(commit=False)
    forum.forum_master = user
    forum.save()
    forum_account = ForumAccount.objects.create(forum=forum, user=user)
    category = Category.create_test_category(forum)
    sub_category = SubCategory.create_test_subcategory(category)
    topic = Topic.create_topic_test(sub_category, forum_account)
    Message.message_test(topic, forum_account)
    return forum
