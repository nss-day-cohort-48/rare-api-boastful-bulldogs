"""rare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rareapi.views import register_user, login_user
from rareapi.views import CategoryView
from rareapi.views import CommentView
from rareapi.views import PostView
from rareapi.views import ProfileView
from rareapi.views import TagView
from rareapi.views import RareUserView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostView, 'post')
router.register(r'categories', CategoryView, 'category')
router.register(r'tags', TagView, "tag")
router.register(r'comments', CommentView, 'comment')
router.register(r'profile', ProfileView, 'profile')
router.register(r'users', RareUserView, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
