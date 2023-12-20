from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from forum.models import Forum, Topic


class CreateForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ["name", "theme", "description"]


class CreateTopic(forms.ModelForm):
    message = forms.CharField(label="Message", max_length=1000, widget=CKEditorUploadingWidget)

    class Meta:
        model = Topic
        fields = ["title", "message"]
