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
from socialmedia.api.pagination import LimitOffsetPagination, get_paginated_response


class SubscribeDetailApi(ApiAuthMixin, APIView):

    @extend_schema(responses=None)
    def delete(self, request, username):
        try:
            unsubscribe(user = request.user, username = username)
        except Exception as ex:
            return Response({"detail": "database Error - " + str(ex)},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

class SubscribeListApi(ApiAuthMixin, APIView):
    
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class InputSubSerializer(serializers.Serializer):
        username = serializers.CharField()


    class OutputSubSerializer(serializers.ModelSerializer):


        class Meta:
            model = Connection
            fields = ['subscriber', 'target']


    class OutputProfileForSubscribeSerializer(serializers.ModelSerializer):

        username = serializers.SerializerMethodField('get_username')
        class Meta:
            model = Profile
            fields = ['username', 'bio', 'subscribers_count', 'posts_count']

        def get_username(self, profile: Profile) -> str:
            return profile.user.username

    @extend_schema(responses=OutputProfileForSubscribeSerializer)
    def get(self, request):

        queryset = get_profiles()
        return get_paginated_response(pagination_class=self.Pagination,
                        serializer_class=self.OutputProfileForSubscribeSerializer,
                        queryset=queryset, request=request, view= self)

    @extend_schema(request=InputSubSerializer, responses=OutputSubSerializer)
    def post(self, request):

        try:
            serializer = self.InputSubSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data.get("username")
            subscription = subscribe(user = request.user, username = username)
        except Exception as err:
            return Response({"detail": "database Error - " + str(err)},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(self.OutputSubSerializer(subscription).data, status=status.HTTP_201_CREATED)