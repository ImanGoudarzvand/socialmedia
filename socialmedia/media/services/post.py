from socialmedia.media.models import Post, Connection
from socialmedia.users.models import User, Profile
from django.db import transaction
from django.db.models import QuerySet
from django.utils.text import slugify
from django.core.cache import cache

def count_follower(*, user: User) -> int:
    return Connection.objects.filter(target=user).count()


def count_following(*, user: User) -> int:
    return Connection.objects.filter(subscriber=user).count()

def count_posts(*, user: User) -> int:
    return Post.objects.filter(author=user).count()

def cache_profile(*, user: User) -> None:
    profile = {
            "posts_count": count_posts(user=user),
            "subscribers_count": count_follower(user=user),
            "subscriptions_count": count_following(user=user),
            }
    cache.set(f"profile_{user}", profile, timeout=None)


def subscribe(*, user: User, username: str) -> QuerySet[Connection]:
    target = User.objects.get(username=username)
    sub = Connection(subscriber=user, target=target)
    sub.full_clean()
    sub.save()
    cache_profile(user=user)    
    return sub


def unsubscribe(*, user: User, username: str) -> dict:
    target = User.objects.get(username=username)
    Connection.objects.get(subscriber=user, target=target).delete()
    cache_profile(user=user)

@transaction.atomic
def create_post(*, user: User, title: str, content: str) -> QuerySet[Post]:
    post = Post.objects.create(
        author=user, title=title, content=content, slug=slugify(title)
    )
    cache_profile(user=user)
    return post
