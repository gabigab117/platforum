from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from forum.forms import CreateForumForm
from forum.default_data.default_forum_data import create_forum_with_data


@login_required
def create_forum(request):
    """
        Handles the creation of a new forum.

        This view, accessible only to logged-in users, provides a form for creating a new forum. Upon submission of the
        form with valid data (POST request), a new forum is created using the 'create_forum_with_data' function with the
        logged-in user as the forum master. The user is then redirected to the newly created forum. If accessed via a GET
        request, the form for creating a new forum is displayed.

        Args:
            request: The HTTP request object, either GET for displaying the form or POST for submitting form data.

        Returns:
            HttpResponse: Renders the forum creation page with the form or redirects to the new forum's page after creation.
        """
    user = request.user
    if request.method == "POST":
        form = CreateForumForm(request.POST, request.FILES)
        if form.is_valid():
            forum = create_forum_with_data(form, user)
            return redirect("forum:index", slug_forum=forum.slug, pk_forum=forum.pk)
    else:
        form = CreateForumForm()
    return render(request, "creation/create-forum.html", context={"form": form})
