"""View module for handling requests about games"""
from django.contrib.auth.models import User
from rareapi.models.rareUser import RareUser
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post, Category, RareUser


class PostView(ViewSet):
    """postview"""

    def create(self, request):
        """creates a POST
        Args:
            request ([type]): [description]
        Returns:
            [type]: [description]
        """
        user_id = RareUser.objects.get(user=request.auth.user)
        category_id = Category.objects.get(pk=request.data['categoryId'])
        try:
            post = Post.objects.create(
                user_id = user_id,
                category_id = category_id,
                title=request.data['title'],
                publication_date = request.data['date'],
                image_url = request.data['image'],
                content=request.data['content'],
                approved = request.data["approved"]
            
            )
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
        """handles UPDATE"""

        user_id = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)
        
        post.category_id = Category.objects.get(pk=request.data['categoryId'])
        post.title = request.data['title']
        post.content = request.data['content']
        post.publication_date = request.data['date']
        post.image_url = request.data['image']
        post.approved = request.data['approved']

        post.save()

        serializer = PostSerializer(post, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        """get all posts"""
        posts = Post.objects.all()

        category_id = request.query_params.get('category', None)

        if category_id is not None:
            posts = posts.filter(category_id=category)

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
        model = User
        fields = ['username', 'email']

class PostSerializer(serializers.ModelSerializer):
    """post serializer"""
    class Meta:
        model = Post
        fields = '__all__'
        # depth = 2

    