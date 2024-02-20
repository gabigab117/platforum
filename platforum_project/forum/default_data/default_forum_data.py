from forum.models import ForumAccount, Category, SubCategory, Topic, Message
from django.db import transaction


def create_forum_with_data(form, user):
    """
        Creates a new forum with initial test data.

        This function initializes a new forum using data from the provided form and sets the given user as the forum
        master. It then creates a forum account for the user, and initializes test data including a category,
        sub-category, topic, and a test message within the forum. The initial test data setup is useful for quick
        deployment and testing of the forum's basic functionality.

        Args:
            form: The form containing the data for creating the forum.
            user: The user who will be set as the forum master.

        Returns:
            Forum: The newly created forum object with initial test data.
        """
    with transaction.atomic():
        forum = form.save(commit=False)
        forum.forum_master = user
        forum.save()
        forum_account = ForumAccount.objects.create(forum=forum, user=user, forum_master=True)
        category = Category.create_test_category(forum)
        sub_category = SubCategory.create_test_subcategory(category)
        topic = Topic.create_topic_test(sub_category, forum_account)
        Message.message_test(topic, forum_account)
    return forum
