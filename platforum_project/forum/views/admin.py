from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from account.models import CustomUser
from forum.models import Forum, Topic, ForumAccount
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
def member_status_view(request, pk_forum, pk_member):
    user: CustomUser = request.user
    forum = get_object_or_404(Forum, pk=pk_forum)
    verify_forum_master_status(account=user.retrieve_forum_account(forum))
    member_account = get_object_or_404(ForumAccount, pk=pk_member)
    member_account.deactivate() if member_account.active else member_account.activate()
    return redirect("forum:admin-members", slug_forum=forum.slug, pk_forum=forum.pk)
