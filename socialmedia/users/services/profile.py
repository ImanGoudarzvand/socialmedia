from socialmedia.users.models import User, Profile

def create_profile(*, user: User, bio: str | None) -> Profile:

    return Profile.objects.create(user = user, bio=bio)
    