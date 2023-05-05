from celery import shared_task
from socialmedia.users.services.profile import database_profile_count_update


@shared_task
def profile_count_update():
    database_profile_count_update()

# @shared_task
# def hello2():
#     print("HIIIIIII")