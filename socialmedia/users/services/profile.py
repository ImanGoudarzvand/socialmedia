from socialmedia.users.models import User, Profile
from django.core.cache import cache

def create_profile(*, user: User, bio: str | None) -> Profile:

    return Profile.objects.create(user = user, bio=bio)
    

def database_profile_count_update():
    profiles = cache.keys("profile_*")
    
    for profile_key in profiles:
        username = profile_key.replace("profile_", "") 
        data = cache.get(profile_key)

        try:
            profile = Profile.objects.get(user__username=username)
            profile.posts_count        = data.get("posts_count")
            profile.subscribers_count   = data.get("subscribers_count")
            profile.subscriptions_count = data.get("subscriptions_count")
            profile.save()

        except Exception as ex:
            print(ex)
