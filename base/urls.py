"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework_extensions.routers import ExtendedDefaultRouter

from blog.api import views as blog_api_views

router = ExtendedDefaultRouter()

router.register(r'author', blog_api_views.AuthorViewSet, base_name='author')
router.register(r'category', blog_api_views.CategoryViewSet, base_name='category')
router.register(r'tag', blog_api_views.TagViewSet, base_name='tag')
router.register(r'post', blog_api_views.PostViewSet, base_name='post')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1.0/', include(router.urls)),
]
