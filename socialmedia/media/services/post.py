from socialmedia.media.models import Post, Connection
from socialmedia.users.models import User, Profile
from django.db import transaction
from django.db.models import QuerySet
from django.utils.text import slugify



def subscribe(*, user: User, username: str) -> QuerySet[Connection]:
    target = User.objects.get(username=username)
    sub = Connection(subscriber=user, target=target)
    sub.full_clean()
    sub.save()
    return sub


def unsubscribe(*, user: User, username: str) -> dict:
    target = User.objects.get(username=username)
    Connection.objects.get(subscriber=user, target=target).delete()


@transaction.atomic
def create_post(*, user: User, title: str, content: str) -> QuerySet[Post]:
    post = Post.objects.create(
        author=user, title=title, content=content, slug=slugify(title)
    )
    return post
