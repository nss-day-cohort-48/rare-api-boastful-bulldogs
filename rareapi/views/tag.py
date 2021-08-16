"""View module for handling requests about tag types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework import status
from rareapi.models import Tag
# from django.contrib.auth.models import User
# from rest_framework.decorators import action


class TagView(ViewSet):
    """Level up tag types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag type

        Returns:
            Response -- JSON serialized tag type
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(
                tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all tag types

        Returns:
            Response -- JSON serialized list of tag types
        """
        tags = Tag.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = TagSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations for creating new tags

        Returns:
            Response -- JSON serialized tag instance
        """

        # Create a new Python instance of the Tag class
        # and set its properties from what was sent in the
        # body of the request from the client.
        tag = Tag()
        tag.label = request.data["label"]

        # Try to save the new tag to the database, then
        # serialize the tag instance as JSON, and send the
        # JSON as a response to the client request
        try:
            tag.save()
            serializer = TagSerializer(
                tag, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for an tag

        Returns:
            Response -- Empty body with 204 status code
        """

        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]

        tag.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for Tags

    Arguments:
        serializers
    """
    class Meta:
        model = Tag
        fields = ('id', 'label')  # '__all__'
