from django import forms

from forum.models import Forum, Topic


class CreateForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ["name", "theme", "description"]


class CreateTopic(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, label="Message", max_length=1000)

    class Meta:
        model = Topic
        fields = ["title", "message"]
