import pytest 
import json
from rest_framework import status
from django.urls import reverse


@pytest.fixture
def create_post(authenticated_api_client):
    def do_create_post(body):
        url_ = reverse('api:media:post')
        return authenticated_api_client.post(url_, json.dumps(body), content_type='application/json')
    return do_create_post



@pytest.mark.django_db
class TestPostCreation:

    def test_authuser_create_post_with_correct_data_return_201(self, create_post, post1):

        # Arrange
        post = post1

        # Act
        response = create_post({"title": post.title, "content": post.title})

        # Assertion
        assert response.status_code == status.HTTP_201_CREATED

    def test_authuser_create_post_with_no_title_input_data_return_400(self, create_post, post1):

        post = post1
        post.title = ""

        response = create_post({"title": post.title, "content": post.content})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_authuser_create_post_with_no_content_input_data_return_400(self, create_post, post1):

        post = post1
        post.content = " "

        response = create_post({"title": post.title, "content": post.content})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def test_unauthuser_create_post_return_401(self, api_client, post1):

        post = post1

        response = api_client.post(reverse('api:media:post'), json.dumps({"title": post.title, "content": post.content}),
        content_type='application.json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_one_user_post_duplicate_title_return_400(self, create_post, post1):

        post1 = post1
        post2 = post1


        response1 = create_post({"title": post1.title, "content": post1.title})
        response2 = create_post({"title": post2.title, "content": post2.title})

        assert response2.status_code == status.HTTP_400_BAD_REQUEST


    def test_different_user_post_duplicate_title_return_400(self, create_post, post1, post2):

        post1 = post1
        post2 = post2
        post2.title = post1.title


        response1 = create_post({"title": post1.title, "content": post1.title})
        response2 = create_post({"title": post2.title, "content": post2.title})

        assert response2.status_code == status.HTTP_400_BAD_REQUEST
