from .profile import create_profile
from django.db.models import QuerySet
from django.db import transaction
from socialmedia.users.models import User

def create_user(*, username: str, password: str) -> QuerySet[User]:

    return User.objects.create_user(username=username, password=password)

@transaction.atomic
def register(*, username: str, password: str, bio: str | None) -> QuerySet[User]:

    user = create_user(username=username, password=password)
    create_profile(bio=bio, user=user)

    return user