from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework_extensions.routers import ExtendedDefaultRouter

from seed.blog.api import views as blog_api_views
from seed.search.api.views import PostSearchView

router = ExtendedDefaultRouter()

router.register(r'author', blog_api_views.AuthorViewSet, base_name='author')
router.register(r'category', blog_api_views.CategoryViewSet, base_name='category')
router.register(r'tag', blog_api_views.TagViewSet, base_name='tag')
router.register(r'post', blog_api_views.PostViewSet, base_name='post')

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/api/v1.0/')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1.0/', include(router.urls)),
    url(r'^api/search/posts/', PostSearchView.as_view(), name='search-posts'),
]
