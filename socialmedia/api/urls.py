from django.urls import path, include


urlpatterns = [

    path('users/', include(('socialmedia.users.urls', 'users'))),
    path('auth/', include(('socialmedia.authentication.urls', 'authentication'))),
    path('media/', include(('socialmedia.media.urls', 'media'))),


] 