"""View module for handling requests about games"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models.rareUser import RareUser
from rareapi.models import Post, Category


class PostView(ViewSet):
    """postview"""

    def create(self, request):
        """creates a POST
        Args:
            request ([type]): [description]
        Returns:
            [type]: [description]
        """
        user = RareUser.objects.get(user=request.auth.user)
        category_id = Category.objects.get(pk=request.data['category_id'])
        post = Post()
        post.user = user
        post.category = category_id
        post.title=request.data['title']
        post.publication_date = request.data['publication_date']
        post.image_url = request.data['image_url']
        post.content=request.data['content']
        post.approved = request.data["approved"]

        try:
            post.save()
            post.tags.set(request.data["tags"])
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

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
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk):
        """handles PUT"""

        user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)

        post.category = Category.objects.get(pk=request.data['categoryId'])
        post.title = request.data['title']
        post.content = request.data['content']
        post.publication_date = request.data['publication_date']
        post.image_url = request.data['image_url']
        post.approved = request.data['approved']
        post.tags = request.data['tags']

        post.save()

        serializer = PostSerializer(post, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        """get all posts"""
        posts = Post.objects.all()

        category= request.query_params.get('category', None)

        if category is not None:
            posts = posts.filter(category=category)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk):
        """delete"""
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostCategorySerializer(serializers.ModelSerializer):
    """ post category serializer """
    class Meta:
        model = Category
        fields = ['label']

class PostUserSerializer(serializers.ModelSerializer):
    """post user serializer"""
    class Meta:
        model = RareUser
        fields = ['full_name']

class PostSerializer(serializers.ModelSerializer):
    """post serializer"""
    user = PostUserSerializer(many=False)
    category = PostCategorySerializer(many=False)
    class Meta:
        model = Post
        fields = ['id', 'user', 'category', 'title', 'publication_date', 'image_url','content', 'content', 'approved', 'tags']
        depth = 1
