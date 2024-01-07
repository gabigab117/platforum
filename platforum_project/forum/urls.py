from django.urls import path
from .views import create_forum, index, sub_category_view, add_topic, topic_view, update_message, delete_message, \
    personal_messaging, conversation_view, update_message_conversation, delete_message_conversation, profile_forum, \
    signup_forum, members_list_view, pin_topic, display_members, member_status_view, member_view, builder_view, \
    delete_category_view, delete_subcategory_view, update_category_view, update_subcategory_view, start_conversation, \
    index_admin_view, notifications_view, delete_notifications

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
    path('<str:slug_forum>/<int:pk_forum>/start-conversation/<int:pk_member>/', start_conversation,
         name="start-conversation"),
    path(
        '<str:slug_forum>/<int:pk_forum>/update-message/<str:slug_conversation>/<int:pk_conversation>/<int:pk_message>',
        update_message_conversation,
        name="update-message-conversation"),
    path('<int:pk_forum>/delete-message-conversation/<int:pk_conversation>/<int:pk_message>/',
         delete_message_conversation,
         name="delete-message-conversation"),
    path('<str:slug_forum>/<int:pk_forum>/profile/', profile_forum, name="profile"),
    path('<str:slug_forum>/<int:pk_forum>/members-list/', members_list_view, name="members-list"),
    path('<str:slug_forum>/<int:pk_forum>/<int:pk_member>/', member_view, name="member"),
    path("<str:slug_forum>/<int:pk_forum>/notifications/", notifications_view, name="alerts"),
    path('<int:pk_forum>/delete-notifications/', delete_notifications, name="delete-alerts"),

    # Admin Part
    path('<str:slug_forum>/<int:pk_forum>/admin/index', index_admin_view, name="admin-index"),
    path('<int:pk_forum>/<int:pk_topic>/pin/', pin_topic, name="pin"),
    path('<str:slug_forum>/<int:pk_forum>/admin/members/', display_members, name="admin-members"),
    path('<int:pk_forum>/<int:pk_member>/admin/member-status/', member_status_view, name="admin-member-status"),
    path('<str:slug_forum>/<int:pk_forum>/admin/builder/', builder_view, name="builder"),
    path('<int:pk_forum>/<int:pk_category>/admin/delete-category/', delete_category_view, name="delete-category-admin"),
    path('<int:pk_forum>/<int:pk_subcategory>/admin/delete-subcategory/', delete_subcategory_view,
         name="delete-subcategory-admin"),
    path('<str:slug_forum>/<int:pk_forum>/admin/update-category/<int:pk_category>/', update_category_view,
         name="admin-update-category"),
    path('<str:slug_forum>/<int:pk_forum>/admin/update-subcategory/<int:pk_subcategory>/', update_subcategory_view,
         name="admin-update-subcategory"),
]
