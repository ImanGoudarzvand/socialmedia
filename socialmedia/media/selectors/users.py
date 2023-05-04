from socialmedia.users.models import Profile
from django.db.models import QuerySet

def get_profiles() -> QuerySet[Profile] | None :
    return Profile.objects.select_related('user').all()
