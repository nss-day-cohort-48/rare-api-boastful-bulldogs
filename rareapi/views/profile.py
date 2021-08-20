"""View module for handling requests about park areas"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import RareUser


class ProfileView(ViewSet):
    """Gamer can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and events
        """
        rare_user = RareUser.objects.get(user=request.auth.user)
        # gamer = Gamer.objects.get(user=request.auth.user)
        # events = Event.objects.filter(attendees=gamer)
        profiles = RareUser.objects.all()
        # Support filtering comments by postId
        #    http://localhost:8000/profile?userId=1
        #
        # Support filtering profiles by user
        user = self.request.query_params.get('userId', None)
        if user is not None:
            profiles = profiles.get(user__id=user)

            serializer = RareUserSerializer(profiles, many=False, context={'request': request})
            return Response(serializer.data)
        else:
            rare_user = RareUserSerializer(rare_user, many=False, context={'request': request})
            # Manually construct the JSON structure you want in the response
            profile = {}
            profile["user"] = rare_user.data
            # profile["events"] = events.data

            return Response(profile)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('username', 'email', 'date_joined', 'is_staff', 'first_name')

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""

    user = UserSerializer(many=False)
    
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url', 'full_name')
