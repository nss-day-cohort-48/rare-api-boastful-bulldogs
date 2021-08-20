"""View module for handling requests about park areas"""
from django.contrib.auth.models import User
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models.rareUser import RareUser
from rareapi.models.rareUser import RareUser


class RareUserView(ViewSet):
    """Gamer can see profile information"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/posts/2
            #
            # The `2` at the end of the route becomes `pk`
            user = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and events
        """
        users = RareUser.objects.all()
        # gamer = Gamer.objects.get(user=request.auth.user)
        # events = Event.objects.filter(attendees=gamer)

        # events = EventSerializer(
        #     events, many=True, context={'request': request})
        # gamer = GamerSerializer(
        #     gamer, many=False, context={'request': request})
        serializer = RareUserSerializer(
            users, many=True, context={'request': request})
        # Manually construct the JSON structure you want in the response
        # profile = {}
        # profile["user"] = user.data
        # profile["events"] = events.data

        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('is_staff', 'is_active')


class RareUserSerializer(serializers.ModelSerializer):
    """post user serializer"""
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ['id', 'full_name', 'user', 'bio', 'profile_image_url']
