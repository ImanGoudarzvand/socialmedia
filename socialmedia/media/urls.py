from django.urls import path, include
from socialmedia.media.apis.subscription import SubscribeDetailApi, SubscribeListApi
from socialmedia.media.apis.post import PostDetailApi, PostListApi


urlpatterns = [
    path('unsubscribe/<str:username>/', SubscribeDetailApi.as_view(), name='unsubscribe'),
    path('subscribe/', SubscribeListApi.as_view(), name='subscribe'),
    path('posts/', PostListApi.as_view(), name='post'),
    path('posts/<slug:slug>', PostDetailApi.as_view(), name='post_detail'),
]