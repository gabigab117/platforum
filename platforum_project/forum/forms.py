from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from forum.models import Forum, Topic, Message


class CreateForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ["name", "theme", "description"]


class CreateTopic(forms.ModelForm):
    message = forms.CharField(label="", max_length=10000, widget=CKEditorUploadingWidget)

    class Meta:
        model = Topic
        fields = ["title", "message"]


class PostMessage(forms.Form):
    message = forms.CharField(max_length=10000, label="", widget=CKEditorUploadingWidget)
