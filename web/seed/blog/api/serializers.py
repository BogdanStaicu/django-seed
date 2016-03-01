from rest_framework import serializers
from seed.blog.models import Author, Category, Post, Tag


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class PostSerializer(serializers.ModelSerializer):
    categories_list = serializers.StringRelatedField(source='categories', many=True, read_only=True)
    tags_list = serializers.StringRelatedField(source='tags', many=True,  read_only=True)
    class Meta:
        model = Post
        write_only_fields = ['categories', 'tags']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
