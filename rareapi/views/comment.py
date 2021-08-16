"""View module for handling requests about comments"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.fields import BooleanField
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from django.db.models import Count, Case, When
from rareapi.models import RareUser, Comment, Post


class CommentView(ViewSet):
    """Rare comments"""

    def create(self, request):
        """Handle POST operations for comments
        Returns: Response --JSON serialized event instance
        """
        author = RareUser.objects.get(user=request.auth.user)

        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = request.data["createdOn"]
        comment.author = author

        post = Post.objects.get(pk=request.data["postId"])
        comment.post = post

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment
        Returns: Response --JSON serialized comment instance
        """
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        """Handle PUT requests for a comment
        Returns: Response --Empty body with 204 status code
        """
        author = RareUser.objects.get(user=request.auth.user)

        comment = Comment.objects.get(pk=pk)
        comment.content = request.data["content"]
        comment.created_on = request.data["createdOn"]
        comment.author = author

        post = Post.objects.get(pk=request.data["postId"])
        comment.post = post
        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single comment
        Returns: Respons -- 200, 404, or 500 status code
        """
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle GET requests to comments resource
        Returns: Response --JSON serialized list of comments
        """
        # Get the current authenticated user
        # author = RareUser.objects.get(user=request.auth.user)

        comments = Comment.objects.all()

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)






class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comment"""
    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1
