"""API URL Configuration"""
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from apps.users import views as users_views
from apps.posts import views as posts_views

urlpatterns = [
    path("signup/", users_views.SignupAPIView.as_view(), name='signup'),
    path("login/", users_views.LoginAPIView.as_view(), name='login'),

    path("posts/", posts_views.PostListAPIView.as_view(), name='post_list'),
    path("posts/create/", posts_views.PostCreateAPIView.as_view(), name='post_create'),
    path("posts/<int:pk>/", posts_views.PostRetrieveUpdateDestroyAPIView.as_view(), name='post_detail'),
    path("posts/<int:pk>/like/", posts_views.LikeCreateAPIView.as_view(), name='like'),
    path("posts/<int:pk>/unlike/", posts_views.LikeDestroyAPIView.as_view(), name='unlike'),
    path("analitics/", posts_views.PostsAnalyticsAPIView.as_view(), name='analytics'),
    ]
