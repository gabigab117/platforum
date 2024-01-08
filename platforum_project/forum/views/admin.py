from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from account.models import CustomUser
from forum.forms import CreateCategory, CategoryForm, SubCategoryForm, ForumUpdateThumbnail, TopicUpdateForm
from forum.models import Forum, Topic, ForumAccount, Category, SubCategory, Message
from platforum_project.func.security import verify_forum_master_status


@login_required
def index_admin_view(request, slug_forum, pk_forum):
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
    # Créer des catégories auxquelles je rattache des sous-catégories
    # formulaire ==> nom catégorie, et des sous catégories
    # supprimer catégorie ou sous catégorie
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
            SubCategory.objects.create(name=form.cleaned_data["sub_1"], category=category,
                                       index=form.cleaned_data["index_1"])
            if form.cleaned_data["sub_2"]:
                SubCategory.objects.create(name=form.cleaned_data["sub_2"], category=category,
                                           index=form.cleaned_data["index_2"])
            if form.cleaned_data["sub_3"]:
                SubCategory.objects.create(name=form.cleaned_data["sub_3"], category=category,
                                           index=form.cleaned_data["index_3"])
            if form.cleaned_data["sub_4"]:
                SubCategory.objects.create(name=form.cleaned_data["sub_4"], category=category,
                                           index=form.cleaned_data["index_4"])
            if form.cleaned_data["sub_5"]:
                SubCategory.objects.create(name=form.cleaned_data["sub_5"], category=category,
                                           index=form.cleaned_data["index_5"])
            return redirect(request.path)
    else:
        form = CreateCategory()
    return render(request, "admin-forum/builder.html", context={"forum": forum,
                                                                "account": account,
                                                                "categories": categories,
                                                                "form": form})


@login_required
@require_POST
def delete_category_view(request, pk_forum, pk_category):
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_forum_master_status(account=user.retrieve_forum_account(forum))
    Category.objects.get(pk=pk_category).delete()
    return redirect("forum:builder", slug_forum=forum.slug, pk_forum=forum.pk)


@login_required
@require_POST
def delete_subcategory_view(request, pk_forum, pk_subcategory):
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_forum_master_status(account=user.retrieve_forum_account(forum))
    SubCategory.objects.get(pk=pk_subcategory).delete()
    return redirect("forum:builder", slug_forum=forum.slug, pk_forum=forum.pk)


@login_required
def update_category_view(request, slug_forum, pk_forum, pk_category):
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
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    verify_forum_master_status(account)
    subcategory = get_object_or_404(SubCategory, pk=pk_subcategory)

    if request.method == "POST":
        form = SubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect("forum:builder", slug_forum=forum.slug, pk_forum=pk_forum)
    else:
        form = SubCategoryForm(instance=subcategory)
    return render(request, "admin-forum/subcategory-update.html", context={"forum": forum, "account": account,
                                                                           "subcategory": subcategory, "form": form})


@login_required
def update_topic(request, slug_forum, pk_forum, pk_topic):
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
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    account = user.retrieve_forum_account(forum)
    verify_forum_master_status(account)
    topic = get_object_or_404(Topic, pk=pk_topic)
    topic.delete()
    return redirect("forum:sub-category", slug_forum=forum.slug, pk_forum=forum.pk, pk=topic.sub_category.pk,
                    slug_sub_category=topic.sub_category.slug)
