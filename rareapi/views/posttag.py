"""View module for handling requests about post_tag types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework import status
from rareapi.models import PostTag, Post, Tag
# from django.contrib.auth.models import User
# from rest_framework.decorators import action


class PostTagView(ViewSet):
    """Level up post_tag types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post_tag type

        Returns:
            Response -- JSON serialized post_tag type
        """
        try:
            post_tag = PostTag.objects.get(pk=pk)
            serializer = PostTagSerializer(
                post_tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all post_tag types

        Returns:
            Response -- JSON serialized list of post_tag types
        """
        tags = PostTag.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PostTagSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations for creating new tags

        Returns:
            Response -- JSON serialized post_tag instance
        """

        # Create a new Python instance of the PostTag class
        # and set its properties from what was sent in the
        # body of the request from the client.
        post_tag = PostTag()
        post_id = Post.objects.get(pk=request.data['post_id'])
        post_tag.post = post_id
        tag_id = Tag.objects.get(pk=request.data['tag_id'])
        post_tag.tag = tag_id

        # Try to save the new post_tag to the database, then
        # serialize the post_tag instance as JSON, and send the
        # JSON as a response to the client request
        try:
            post_tag.save()
            serializer = PostTagSerializer(
                post_tag, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for an post_tag

        Returns:
            Response -- Empty body with 204 status code
        """

        post_tag = PostTag.objects.get(pk=pk)
        post_tag.post = request.data["post_id"]
        post_tag.tag = request.data["tag_id"]

        post_tag.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post_tag = PostTag.objects.get(pk=pk)
            post_tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PostTag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class PostSerializer(serializers.ModelSerializer):
#     """post serializer"""
#     user = PostUserSerializer(many=False)
#     category = PostCategorySerializer(many=False)

#     class Meta:
#         model = Post
#         fields = ['id', 'user', 'category', 'title', 'publication_date',
#                   'image_url', 'content', 'content', 'approved', 'tags', 'owner']
#         depth = 1

class PostTagSerializer(serializers.ModelSerializer):
    """JSON serializer for Tags

    Arguments:
        serializers
    """
    class Meta:
        model = PostTag
        fields = '__all__'
        depth = 2
