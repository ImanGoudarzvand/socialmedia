from socialmedia.users.services.user import create_user
from socialmedia.users.models import User, Profile
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from typing import Callable
from pytest_factoryboy import register
import pytest
import json


@pytest.fixture
def get_the_profile(authenticated_api_client) -> Callable[None, Response]:
    def do_get_profile():
        url_ = reverse('api:users:profile')
        return authenticated_api_client.get(url_,content_type="application/json")
    return do_get_profile


@pytest.mark.django_db
class TestProfileRetrieve:

    def test_authuser_retrieve_profile_return_200(self, get_the_profile):

        # Act
        response = get_the_profile()

        # Assertion
        assert response.status_code == status.HTTP_200_OK
        assert response.data["bio"] is not None 

    def test_unauth_retrieve_profile_return_401(self, api_client):

        # Act
        response = api_client.get(reverse('api:users:profile'),content_type="application/json")

        # Assertion
        assert response.status_code == status.HTTP_401_UNAUTHORIZED