from rest_framework.request import Request
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from socialmedia.users.models import User, Profile
from socialmedia.api.mixins import ApiAuthMixin
from drf_spectacular.utils import extend_schema
from socialmedia.media.models import Connection
from socialmedia.media.services.post import subscribe, unsubscribe
from socialmedia.media.selectors.users import get_profiles
from socialmedia.api.pagination import LimitOffsetPagination, get_paginated_response, get_paginated_response_context
from socialmedia.media.models import Post
from socialmedia.media.services.post import create_post
from socialmedia.media.selectors.posts import post_list, post_detail
from django.urls import reverse

class PostListApi(ApiAuthMixin, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 10


    # using serializr as a filtering for input data of the client
    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255, required=False)
        search = serializers.CharField(max_length=255, required=False)
        created_at__range = serializers.CharField(max_length=255, required=False)
        author__in = serializers.CharField(max_length=255, required=False)
        slug = serializers.CharField(max_length=255, required=False)
        content = serializers.CharField(max_length=500, required=False)



    class InputPostSerializer(serializers.Serializer):
        content = serializers.CharField(max_length=500)
        title = serializers.CharField(max_length=255)

    class OutputPostSerializer(serializers.ModelSerializer):

        author = serializers.SerializerMethodField('get_author')
        url = serializers.SerializerMethodField('get_url')

        class Meta:
            model = Post
            fields = ['author', 'url']

        def get_author(self, post: Post) -> str :
            return post.author.username

        def get_url(self, post) -> str:
            request = self.context.get("request")
            path = reverse("api:media:post_detail", args=[post.slug])
            return request.build_absolute_uri(path)

    @extend_schema(request=InputPostSerializer, responses=OutputPostSerializer)
    def post(self, request):
        serializer = self.InputPostSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            queryset = create_post(
                user= request.user,
                content= serializer.validated_data.get("content"),
                title = serializer.validated_data.get("title")
            )
        except Exception as ex:
            return Response(
                {"detail": "Database Error - " + str(ex)},
                status = status.HTTP_400_BAD_REQUEST,
            )
        return Response(self.OutputPostSerializer(queryset, context={"request": request}).data, status=status.HTTP_201_CREATED)

    @extend_schema(parameters=[FilterSerializer], responses=OutputPostSerializer)
    def get(self, request: Request):
        filters_serializer = self.FilterSerializer(data = request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        try:
            queryset = post_list(filters = filters_serializer.validated_data, user=request.user)
        except Exception as err:
            return Response({"detail": "Filter Error - " + str(err)}, status=status.HTTP_400_BAD_REQUEST)


        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutputPostSerializer,
            queryset=queryset,
            request=request,
            view=self
        )

    
class PostDetailApi(ApiAuthMixin, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutputDetailSerializer(serializers.ModelSerializer):

        author = serializers.SerializerMethodField('get_author')
        class Meta:
            model = Post
            fields = ['author', 'slug', 'title', 'content', 'created_at', 'updated_at']

        def get_author(self, post) -> str:
            return post.author.username

    @extend_schema(responses=OutputDetailSerializer)
    def get(self, request, slug):

        try:
            queryset = post_detail(slug = slug, user = request.user)
        except Exception as err:
            return Response(
                {"detail": "filter Error - " + str(err)},
                status = status.HTTP_400_BAD_REQUEST
            )

        return Response(self.OutputDetailSerializer(queryset).data)