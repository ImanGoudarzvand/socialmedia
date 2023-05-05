import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import factory
from pytest_factoryboy import register
from socialmedia.users.models import User, Profile
from socialmedia.media.models import Connection, Post
from faker import Faker
from django.utils import timezone
faker = Faker()


@register
class UserFactory(factory.django.DjangoModelFactory):

    # username = factory.Iterator(["user1", "user2", "user3"])
    username = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')
    
    class Meta:
        model = User


@register
class ProfileFactory(factory.django.DjangoModelFactory):
    user                 = factory.SubFactory(UserFactory)
    posts_count          = factory.LazyAttribute(lambda _: 0 )
    subscriptions_count  = factory.LazyAttribute(lambda _: 0 )
    subscribers_count    = factory.LazyAttribute(lambda _: 0 )
    bio                  = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
 
    class Meta:
        model = Profile



# user object for testing services/selectors of user api


@register(_name='ConnectionFactory')
class ConnectionFactory(factory.django.DjangoModelFactory):

    target = factory.SubFactory(UserFactory)
    subscriber = factory.SubFactory(UserFactory)

    class Meta:
        model = Connection

@register()
class PostFactory(factory.django.DjangoModelFactory):
        
    slug = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    title = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    content = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    created_at = factory.LazyAttribute(lambda _: f'{timezone.now()}')
    updated_at = factory.LazyAttribute(lambda _: f'{timezone.now()}')
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Post




@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture 
def user1(user):
    return user

@pytest.fixture 
def user2(user):
    return user

@pytest.fixture 
def get_profile(profile):
    return profile

@pytest.fixture
def authenticated_api_client(get_profile):
    get_profile
    authenticated_client = APIClient()
    refresh = RefreshToken.for_user(get_profile.user)
    authenticated_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return authenticated_client


@pytest.fixture
def post1(post):
    return post

@pytest.fixture
def post2(post):
    return post