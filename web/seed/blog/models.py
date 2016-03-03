from __future__ import unicode_literals
from django.db import models
from django.dispatch import receiver


class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    bio = models.TextField()
    def __str__(self):
        return self.name


class Category(models.Model):
    cat_name = models.CharField('Category Name', max_length=50)
    cat_description = models.CharField('Category Description', max_length=255)
    def __str__(self):
        return self.cat_name
    class Meta:
        verbose_name_plural='Categories'


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    tag_description = models.CharField(max_length=255)
    def __str__(self):
        return self.tag_name

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    author = models.ForeignKey(Author)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.title


@receiver(models.signals.post_save, sender=Post, dispatch_uid='seed.blog.post_update')
def add_card_source(instance, *args, **kwargs):
    from seed.search.models import PostES
    PostES.index_post(instance)