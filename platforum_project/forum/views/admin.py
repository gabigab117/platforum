from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from account.models import CustomUser
from forum.forms import CreateCategory
from forum.models import Forum, Topic, ForumAccount, Category, SubCategory
from platforum_project.func.security import verify_forum_master_status


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
    return render(request, "admin/members.html", context={"forum": forum, "account": account, "members": members})


@login_required
@require_POST
def member_status_view(request, pk_forum, pk_member):
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_forum_master_status(account=user.retrieve_forum_account(forum))
    member_account = get_object_or_404(ForumAccount, pk=pk_member)
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
            category = Category.objects.create(name=form.cleaned_data["category"], forum=forum)
            SubCategory.objects.create(name=form.cleaned_data["sub_1"], category=category)
            if form.cleaned_data["sub_2"]:
                SubCategory.objects.create(name=form.cleaned_data["sub_2"], category=category)
            if form.cleaned_data["sub_3"]:
                SubCategory.objects.create(name=form.cleaned_data["sub_3"], category=category)
            if form.cleaned_data["sub_4"]:
                SubCategory.objects.create(name=form.cleaned_data["sub_4"], category=category)
            if form.cleaned_data["sub_5"]:
                SubCategory.objects.create(name=form.cleaned_data["sub_5"], category=category)
            return redirect(request.path)
    else:
        form = CreateCategory()
    return render(request, "admin/builder.html", context={"forum": forum,
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
