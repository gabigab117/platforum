from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from forum.models import Forum, Topic, Message, ForumAccount, Category, SubCategory, Conversation

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class CreateForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ["name", "theme", "description", "thumbnail"]


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


class CreateCategory(forms.Form):
    category = forms.CharField(max_length=40, label="Catégorie")
    index_category = forms.IntegerField(label="Index")
    sub_1 = forms.CharField(max_length=40, label="Sous-catégorie 1")
    index_1 = forms.IntegerField(label="Index 1")
    sub_2 = forms.CharField(max_length=40, label="Sous-catégorie 2", required=False)
    index_2 = forms.IntegerField(label="Index 2", required=False)
    sub_3 = forms.CharField(max_length=40, label="Sous-catégorie 3", required=False)
    index_3 = forms.IntegerField(label="Index 3", required=False)
    sub_4 = forms.CharField(max_length=40, label="Sous-catégorie 4", required=False)
    index_4 = forms.IntegerField(label="Index 4", required=False)
    sub_5 = forms.CharField(max_length=40, label="Sous-catégorie 5", required=False)
    index_5 = forms.IntegerField(label="Index 5", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("category", css_class="col-md-10"),
                Column("index_category", css_class="col-md-2"),
            ),
            Row(
                Column("sub_1", css_class="col-md-10"),
                Column("index_1", css_class="col-md-2"),
            ),
            Row(
                Column("sub_2", css_class="col-md-10"),
                Column("index_2", css_class="col-md-2"),
            ),
            Row(
                Column("sub_3", css_class="col-md-10"),
                Column("index_3", css_class="col-md-2"),
            ),
            Row(
                Column("sub_4", css_class="col-md-10"),
                Column("index_4", css_class="col-md-2"),
            ),
            Row(
                Column("sub_5", css_class="col-md-10"),
                Column("index_5", css_class="col-md-2"),
            ),
            Row(Column(Submit('submit', "Valider", css_class="btn btn-success center"), css_class="text-center"))
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "index"]


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ["name", "index"]


class ConversationForm(forms.ModelForm):
    message = forms.CharField(widget=CKEditorUploadingWidget, label="", max_length=10000)

    class Meta:
        model = Conversation
        fields = ["subject", "message"]


class ForumUpdateThumbnail(forms.ModelForm):
    thumbnail = forms.ImageField(label="")

    class Meta:
        model = Forum
        fields = ["thumbnail"]


class TopicUpdateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "sub_category"]

    def __init__(self, forum, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sub_category"].queryset = SubCategory.objects.filter(category__forum=forum)
