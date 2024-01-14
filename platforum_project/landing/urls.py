from django.urls import path

from landing.views import index, forums_list_view, my_forums_list_view, forum_documentation_view, \
    admin_documentation_view

app_name = "landing"
urlpatterns = [
    path('', index, name="index"),
    path('forums-list/', forums_list_view, name="forums-list"),
    path('my-forums-list/', my_forums_list_view, name="my-forums-list"),
    path('documentation-forum/', forum_documentation_view, name="documentation-forum"),
    path('admin-documentation/', admin_documentation_view, name="admin-documentation"),
]
