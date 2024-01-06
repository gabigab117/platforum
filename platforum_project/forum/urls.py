from django.urls import path
from .views import create_forum, index, sub_category_view, add_topic, topic_view, update_message, delete_message, \
    personal_messaging, conversation_view, update_message_conversation, delete_message_conversation, profile_forum, \
    signup_forum, members_list_view, pin_topic, display_members, member_status_view

app_name = "forum"
urlpatterns = [
    path('create-forum/', create_forum, name="create-forum"),
    path('<str:slug_forum>/<int:pk_forum>/signup/', signup_forum, name="signup"),
    path('<str:slug_forum>/<int:pk_forum>/index/', index, name="index"),
    path('<str:slug_forum>/<int:pk_forum>/sub-category/<int:pk>/<str:slug_sub_category>', sub_category_view,
         name="sub-category"),
    path('<str:slug_forum>/<int:pk_forum>/<int:pk>/<str:slug_sub_category>/add/', add_topic, name="add-topic"),
    path('<str:slug_forum>/<int:pk_forum>/<int:pk>/<str:slug_sub_category>/<int:pk_topic>/<str:slug_topic>/',
         topic_view,
         name="topic"),
    path(
        '<str:slug_forum>/<int:pk_forum>/<int:pk>/<str:slug_sub_category>/<int:pk_topic>/<str:slug_topic>/<int:pk_message>/',
        update_message,
        name="update-message"),
    path('<int:pk_forum>/delete-message/<int:pk_topic>/<int:pk_message>/', delete_message, name="delete-message"),
    path('<str:slug_forum>/<int:pk_forum>/private-messaging/', personal_messaging, name="private-messaging"),
    path('<str:slug_forum>/<int:pk_forum>/private-messaging/<str:slug_conversation>/<int:pk_conversation>/',
         conversation_view,
         name="conversation"),
    path(
        '<str:slug_forum>/<int:pk_forum>/update-message/<str:slug_conversation>/<int:pk_conversation>/<int:pk_message>',
        update_message_conversation,
        name="update-message-conversation"),
    path('<int:pk_forum>/delete-message-conversation/<int:pk_conversation>/<int:pk_message>/',
         delete_message_conversation,
         name="delete-message-conversation"),
    path('<str:slug_forum>/<int:pk_forum>/profile/', profile_forum, name="profile"),
    path('<str:slug_forum>/<int:pk_forum>/members-list/', members_list_view, name="members-list"),

    # Admin Part
    path('<int:pk_forum>/<int:pk_topic>/pin/', pin_topic, name="pin"),
    path('<str:slug_forum>/<int:pk_forum>/admin/members/', display_members, name="admin-members"),
    path('<int:pk_forum>/<int:pk_member>/admin/member-status/', member_status_view, name="admin-member-status"),
]
