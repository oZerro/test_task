from django.urls import path

from .views import (
    PostAPIView,
    RegistrUserView,
    MyPostAPIView,
    ListUsersAPIView,
    ListUsersSortedCountPostsAPI,
    PostsOneUserAPI,
    AddFolowerView,
    ListFollowersAPIVIew,
    ListPostMyFollow,
    UnFollowView,
)


urlpatterns = [
    path('posts/', PostAPIView.as_view(), name="posts"),
    path('register/', RegistrUserView.as_view(), name="register"),
    path('my_posts/', MyPostAPIView.as_view(), name="my_posts"),
    path('all_users/', ListUsersAPIView.as_view(), name="all_users"),
    path('all_users/sorted',
         ListUsersSortedCountPostsAPI.as_view(),
         name="sorted_user"),
    path('posts/user/<int:pk>', PostsOneUserAPI.as_view(), name="post_one_user"),
    path('my_follows/', ListFollowersAPIVIew.as_view(), name="my_follower"),
    path('my_follows/posts', ListPostMyFollow.as_view(), name="my_follow_post"),
    path('follow/<int:pk>', AddFolowerView.as_view(), name="add_follower"),
    path('un_follow/<int:pk>', UnFollowView.as_view(), name="add_follower"),


]