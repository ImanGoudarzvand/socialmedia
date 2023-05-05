from rest_framework import status
from django.urls import reverse
from rest_framework.response import Response
from typing import Callable
import pytest
import json


@pytest.fixture
def create_test_user(api_client) -> Callable[dict[str, str], Response]:
    def do_create_test_user(body):
        url_ = reverse('api:users:register')
        return api_client.post(url_, json.dumps(body), content_type="application/json")
    return do_create_test_user


@pytest.mark.django_db
class TestUserRegister:
    def test_create_user_return_201(self, create_test_user, user1):

        # Arrange
        user = user1
        user.username = "username_test"

        # Act
        response = create_test_user({"username": user.username, "password" : user.password, "confirm_password": user.password})

        # Assertion
        assert response.data["access"] is not None
        assert response.data["refresh"] is not None 
        assert response.status_code == 201

    def test_create_user_with_no_confirm_password_return_400(self, create_test_user, user1):

        # Arrange
        user = user1
        user.username = "username_test"

        # Act
        response = create_test_user({"username": user.username, "password" : user.password, "confirm_password": ""})


        # Assertion
        assert response.status_code == 400
        assert response.data["detail"] is not None


    def test_create_user_with_no_equallity_beyween_password_and_confirm_password_return_400(self, create_test_user, user1):

        user = user1
        user.username = "username_test"

        # Act
        response = create_test_user({"username":user.username, "password": user.password, "confirm_password": user.password + 'match_breaker'})

        # Assertion
        assert response.status_code == 400
        assert response.data["detail"] is not None