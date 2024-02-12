from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from account.models import CustomUser
from forum.forms import CreateCategory, CategoryForm, SubCategoryForm, ForumUpdateThumbnail, TopicUpdateForm, \
    NewSubCategoryForm
from forum.models import Forum, Topic, ForumAccount, Category, SubCategory, Message
from platforum_project.func.security import verify_forum_master_status


@login_required
def index_admin_view(request, slug_forum, pk_forum):
    """
        Displays the admin view for a specific forum.

        This view function is accessible only to administrators of the forum. It retrieves the forum based on the provided
        primary key and slug. It checks if the logged-in user has an associated forum account and verifies their forum
        master status. The function gathers data about active and banned members, topics, and messages of the forum. If
        a POST request is made, it allows for updating the forum's thumbnail. The gathered data is then passed to the
        admin forum template for rendering.

        Args:
            request: The HTTP request object.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.

        Returns:
            HttpResponse: Renders the admin forum page with context data including the forum, account, form for thumbnail
            update, and lists of active members, banned members, topics, and messages.
        """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    verify_forum_master_status(account)

    active_members = ForumAccount.objects.filter(forum=forum, active=True)
    ban_members = ForumAccount.objects.filter(forum=forum, active=False)
    topics = Topic.objects.filter(sub_category__category__forum=forum)
    messages = Message.objects.filter(topic__sub_category__category__forum=forum)

    if request.method == "POST":
        form = ForumUpdateThumbnail(request.POST, request.FILES, instance=forum)
        if form.is_valid():
            form.save()
            redirect(request.path)
    else:
        form = ForumUpdateThumbnail()
    return render(request, "admin-forum/index.html", context={"forum": forum, "account": account, "form": form,
                                                              "active_members": active_members,
                                                              "ban_members": ban_members, "topics": topics,
                                                              "messages": messages})


@login_required
@require_POST
def pin_topic(request, pk_forum, pk_topic):
    """
        Handles the pinning or unpinning of a topic within a forum.

        Accessible only to users with forum master status, this view toggles the pinned status of a specified topic.
        It first verifies the user's association with the forum and their authority to pin or unpin topics. If the
        topic is currently unpinned, it gets pinned, and vice versa. The function then redirects to the sub-category
        page of the topic.

        Args:
            request: The HTTP request object.
            pk_forum: The primary key of the forum.
            pk_topic: The primary key of the topic to be pinned or unpinned.

        Returns:
            HttpResponse: Redirects to the sub-category page of the topic after toggling its pinned status.
        """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    topic = get_object_or_404(Topic, pk=pk_topic)
    verify_forum_master_status(account)
    topic.pin_topic() if not topic.pin else topic.unpin_topic()
    return redirect("forum:sub-category", slug_forum=forum.slug, pk_forum=forum.pk,
                    pk=topic.sub_category.pk, slug_sub_category=topic.sub_category.slug)


@login_required
def display_members(request, slug_forum, pk_forum):
    """
        Displays the member list for a specific forum.

        This view, intended for forum administrators, retrieves and displays a list of members of a specific forum. It
        checks the requesting user's forum account and their forum master status. The function also provides a search
        functionality to filter members by username. The list of members excludes forum masters.

        Args:
            request: The HTTP request object, potentially containing a search query.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.

        Returns:
            HttpResponse: Renders the forum members page with context data including the forum, the user's forum account,
            and the list of members (filtered by search query if provided).
        """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    verify_forum_master_status(account)
    members = ForumAccount.objects.filter(forum=forum, forum_master=False)

    search = request.GET.get("search")
    if search:
        members = ForumAccount.objects.filter(forum=forum, forum_master=False, user__username__icontains=search)
    return render(request, "admin-forum/members.html", context={"forum": forum, "account": account, "members": members})


@login_required
@require_POST
def member_status_view(request, pk_forum, pk_member):
    """
       Toggles the active status of a forum member.

       This view function, restricted to forum masters, allows toggling the active status (active or banned) of a
       forum member. It first verifies the authority of the requesting user in the forum. The function prevents
       altering the status of forum masters. After changing the member's status, it redirects to either the individual
       member view or the forum's admin members list, based on the POST request data.

       Args:
           request: The HTTP POST request object.
           pk_forum: The primary key of the forum.
           pk_member: The primary key of the member whose status is to be toggled.

       Returns:
           HttpResponse: Redirects to either the individual member view or the forum's admin members list.

       Raises:
           PermissionDenied: If the target member is a forum master.
       """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_forum_master_status(account=user.retrieve_forum_account(forum))
    member_account: ForumAccount = get_object_or_404(ForumAccount, pk=pk_member)
    if member_account.forum_master:
        raise PermissionDenied()
    member_account.deactivate() if member_account.active else member_account.activate()

    if request.POST.get("redirect") == "member-view":
        return redirect("forum:member", slug_forum=forum.slug, pk_forum=forum.pk, pk_member=member_account.pk)
    return redirect("forum:admin-members", slug_forum=forum.slug, pk_forum=forum.pk)


@login_required
def builder_view(request, slug_forum, pk_forum):
    """
       Handles the creation of categories and sub-categories within a forum.

       This view is accessible only to forum masters. It displays existing categories and provides a form to create new
       categories and up to five sub-categories. The form data is used to create new Category and SubCategory objects
       associated with the forum. After creation, it redirects to the same page to allow further creation.

       Args:
           request: The HTTP request object, either GET for displaying the form or POST for submitting the form.
           slug_forum: The slug of the forum (unused in the function but required for URL pattern).
           pk_forum: The primary key of the forum.

       Returns:
           HttpResponse: Renders the forum builder page with context data including the forum, user's forum account,
           existing categories, and the category creation form.
       """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    verify_forum_master_status(account)
    categories = Category.objects.filter(forum=forum)

    if request.method == "POST":
        form = CreateCategory(request.POST)
        if form.is_valid():
            category = Category.objects.create(name=form.cleaned_data["category"], forum=forum,
                                               index=form.cleaned_data["index_category"])
            for i in range(1, 6):
                sub_category_name = form.cleaned_data[f"sub_{i}"]
                if sub_category_name:
                    SubCategory.objects.create(name=sub_category_name, category=category,
                                               index=form.cleaned_data[f"index_{i}"])
            return redirect(request.path)
    else:
        form = CreateCategory()
    return render(request, "admin-forum/builder.html", context={"forum": forum,
                                                                "account": account,
                                                                "categories": categories,
                                                                "form": form})


@login_required
def add_sub_category(request, slug_forum, pk_forum, pk_category):
    """
        Handles the addition of a new sub-category to a specific category in a forum.

        This view is accessible only to forum masters. It provides a form to create a new sub-category within a given
        category of the forum. Upon POST request with valid form data, it creates and saves the new sub-category
        associated with the specified category. After successful creation, it redirects to the forum builder page.

        Args:
            request: The HTTP request object, either GET for displaying the form or POST for submitting the form.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.
            pk_category: The primary key of the category to which the sub-category is to be added.

        Returns:
            HttpResponse: Renders the add sub-category page with context data including the forum, user's forum account,
            the parent category, and the sub-category creation form.
        """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    category = get_object_or_404(Category, pk=pk_category)
    verify_forum_master_status(account)

    if request.method == "POST":
        form = NewSubCategoryForm(request.POST)
        if form.is_valid():
            sub_category = form.save(commit=False)
            sub_category.category = category
            sub_category.save()
            return redirect("forum:builder", slug_forum=forum.slug, pk_forum=forum.pk)
    else:
        form = NewSubCategoryForm()
    return render(request, "admin-forum/add-sub-category.html", context={"forum": forum, "account": account,
                                                                         "category": category, "form": form})


@login_required
@require_POST
def delete_category_view(request, pk_forum, pk_category):
    """
        Handles the deletion of a category within a forum.

        This view is designed for forum masters to delete a specific category from a forum. It ensures that the request
        is a POST request and that the user has forum master status in the specified forum. Upon validation, the specified
        category is deleted. After successful deletion, the function redirects to the forum builder page.

        Args:
            request: The HTTP POST request object.
            pk_forum: The primary key of the forum.
            pk_category: The primary key of the category to be deleted.

        Returns:
            HttpResponse: Redirects to the forum builder page after deletion of the category.
        """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_forum_master_status(account=user.retrieve_forum_account(forum))
    Category.objects.get(pk=pk_category).delete()
    return redirect("forum:builder", slug_forum=forum.slug, pk_forum=forum.pk)


@login_required
@require_POST
def delete_subcategory_view(request, pk_forum, pk_subcategory):
    """
       Handles the deletion of a sub-category within a forum.

       Accessible only to forum masters, this view enables the deletion of a specified sub-category from the forum.
       The function checks that the request is a POST request and that the user has the necessary forum master status.
       It then deletes the sub-category identified by the primary key. Following the deletion, it redirects to the
       forum builder page to continue forum management.

       Args:
           request: The HTTP POST request object.
           pk_forum: The primary key of the forum.
           pk_subcategory: The primary key of the sub-category to be deleted.

       Returns:
           HttpResponse: Redirects to the forum builder page after the successful deletion of the sub-category.
       """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_forum_master_status(account=user.retrieve_forum_account(forum))
    SubCategory.objects.get(pk=pk_subcategory).delete()
    return redirect("forum:builder", slug_forum=forum.slug, pk_forum=forum.pk)


@login_required
def update_category_view(request, slug_forum, pk_forum, pk_category):
    """
        Handles the updating of a category within a forum.

        This view allows forum masters to update the details of an existing category in the forum. It verifies the user's
        forum master status and then provides a form pre-filled with the category's current data. If the form is submitted
        with valid POST data, the category is updated with the new information. The function then redirects to the forum
        builder page.

        Args:
            request: The HTTP request object, either GET for displaying the form or POST for submitting form data.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.
            pk_category: The primary key of the category to be updated.

        Returns:
            HttpResponse: Renders the category update page with context data including the forum, user's forum account,
            the category, and the category update form.
        """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    verify_forum_master_status(account)
    category = get_object_or_404(Category, pk=pk_category)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("forum:builder", slug_forum=forum.slug, pk_forum=pk_forum)
    else:
        form = CategoryForm(instance=category)
    return render(request, "admin-forum/category-update.html", context={"forum": forum, "account": account,
                                                                        "category": category, "form": form})


@login_required
def update_subcategory_view(request, slug_forum, pk_forum, pk_subcategory):
    """
        Handles the updating of a sub-category within a forum.

        This view is accessible only to forum masters and is used for updating the details of an existing sub-category.
        It verifies the forum master status of the user and provides a form pre-populated with the sub-category's current
        data. On receiving valid POST data, the sub-category is updated accordingly. After the update, it redirects to
        the forum builder page for continued forum management.

        Args:
            request: The HTTP request object, either GET for displaying the form or POST for submitting form data.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.
            pk_subcategory: The primary key of the sub-category to be updated.

        Returns:
            HttpResponse: Renders the sub-category update page with context data including the forum, user's forum account,
            the sub-category, and the sub-category update form.
        """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    verify_forum_master_status(account)
    subcategory = get_object_or_404(SubCategory, pk=pk_subcategory)

    if request.method == "POST":
        form = SubCategoryForm(forum, request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect("forum:builder", slug_forum=forum.slug, pk_forum=pk_forum)
    else:
        form = SubCategoryForm(forum, instance=subcategory)
    return render(request, "admin-forum/subcategory-update.html", context={"forum": forum, "account": account,
                                                                           "subcategory": subcategory, "form": form})


@login_required
def update_topic(request, slug_forum, pk_forum, pk_topic):
    """
        Handles the updating of a forum topic.

        This view is accessible to forum masters for updating the details of an existing topic within the forum.
        It verifies the user's status as a forum master and provides a form pre-populated with the topic's current
        information. Upon submission of valid POST data, the topic is updated with the new details. The function then
        redirects to the updated topic page.

        Args:
            request: The HTTP request object, either GET for displaying the form or POST for submitting form data.
            slug_forum: The slug of the forum (unused in the function but required for URL pattern).
            pk_forum: The primary key of the forum.
            pk_topic: The primary key of the topic to be updated.

        Returns:
            HttpResponse: Renders the topic update page with context data including the forum, user's forum account,
            the topic, and the topic update form.
        """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    verify_forum_master_status(account)
    topic = get_object_or_404(Topic, pk=pk_topic)

    if request.method == "POST":
        form = TopicUpdateForm(forum, request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect(topic)
    else:
        form = TopicUpdateForm(forum, instance=topic)
    return render(request, "admin-forum/update-topic.html", context={"forum": forum, "account": account,
                                                                     "topic": topic, "form": form})


@login_required
@require_POST
def delete_topic_view(request, pk_forum, pk_topic):
    """
        Handles the deletion of a topic within a forum.

        This view, accessible only to forum masters, enables the deletion of a specific topic from the forum. It verifies
        the forum master status of the requesting user and then proceeds to delete the topic identified by the primary key.
        After deletion, the function redirects to the sub-category page of the deleted topic, maintaining the forum's
        navigational context.

        Args:
            request: The HTTP POST request object.
            pk_forum: The primary key of the forum.
            pk_topic: The primary key of the topic to be deleted.

        Returns:
            HttpResponse: Redirects to the sub-category page of the deleted topic's forum after successful deletion.
        """
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    verify_forum_master_status(account)
    topic = get_object_or_404(Topic, pk=pk_topic)
    topic.delete()
    return redirect("forum:sub-category", slug_forum=forum.slug, pk_forum=forum.pk, pk=topic.sub_category.pk,
                    slug_sub_category=topic.sub_category.slug)
