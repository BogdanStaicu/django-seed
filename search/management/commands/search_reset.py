from django.conf import settings
from django.core.management import BaseCommand, CommandError
from elasticsearch_dsl.connections import connections

from blog.models import Post
from search.models import PostES


class Command(BaseCommand):
    THREAD_COUNT = 4

    def handle(self, *args, **options):
        es = connections.get_connection()
        self.stdout.write('Deleting all the indices')
        es.indices.delete('blog-search')

        es.indices.create('blog-search', settings.ES_INDICES_SETTINGS)

        for post in Post.objects.all():
            PostES.index_post(post)