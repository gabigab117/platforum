from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from forum.models import Forum, Topic, Message, ForumAccount


class CreateForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ["name", "theme", "description"]


class CreateTopic(forms.ModelForm):
    message = forms.CharField(label="", max_length=10000, widget=CKEditorUploadingWidget)

    class Meta:
        model = Topic
        fields = ["title", "message"]


class PostMessage(forms.ModelForm):
    message = forms.CharField(max_length=10000, label="", widget=CKEditorUploadingWidget)

    class Meta:
        model = Message
        fields = ["message"]


class ProfileUpdateForm(forms.ModelForm):
    thumbnail = forms.ImageField(label="Modifier ma photo de profil")

    class Meta:
        model = ForumAccount
        fields = ["thumbnail"]


class SignupForumForm(forms.ModelForm):
    thumbnail = forms.ImageField(label="Photo de profil", required=False)

    class Meta:
        model = ForumAccount
        fields = ["thumbnail"]
