from django.db.models import QuerySet
from socialmedia.media.models import Post, Connection
from socialmedia.users.models import User
from socialmedia.media.filters import PostFilter


def get_subscribers(*, user:User) -> QuerySet[Connection]:
    return Connection.objects.filter(subscriber=user)

def post_detail(*, slug:str, user:User, self_include:bool = True) -> Post:
    subscribtions = list(Connection.objects.filter(subscriber=user).values_list("target", flat=True))
    if self_include:
        subscribtions.append(user.id)
 
    return Post.objects.select_related('author').get(slug=slug, author__in=subscribtions)

def post_list(*, filters=None, user:User, self_include:bool = True) -> QuerySet[Post]:
    filters = filters or {}
    subscribtions = list(Connection.objects.filter(subscriber=user).values_list("target", flat=True))
    if self_include:
        subscribtions.append(user.id)
    if subscribtions:
        qs = Post.objects.select_related('author').filter(author__in=subscribtions)
        return PostFilter(filters, qs).qs
    return Post.objects.none()
