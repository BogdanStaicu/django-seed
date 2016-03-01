from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from serializers import AuthorSerializer, TagSerializer, CategorySerializer, PostSerializer

from seed.blog.models import Author, Category, Post, Tag

class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    # permission_classes = (,)

    def get_queryset(self):
        queryset = Author.objects.all()
        return queryset


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    # permission_classes = (,)

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    # permission_classes = (,)

    def get_queryset(self):
        queryset = Tag.objects.all()
        return queryset