from elasticsearch import NotFoundError
from elasticsearch_dsl import DocType, Q, F
from elasticsearch_dsl.document import DOC_META_FIELDS, META_FIELDS
from elasticsearch_dsl.field import Boolean, Integer, String, Nested, Date, Object

from blog.models import Post

class AlreadyExistsError(Exception):
    """
    Exception raised when object already exists in elasticsearch.
    """


class BaseESMixin(object):
    @classmethod
    def get_or_create(cls, id, save=False, raise_error=False):
        if not id:
            raise ValueError('id cannot be empty')
        id_str = unicode(id)
        obj = None
        created = False
        try:
            obj = cls.get(id=id_str)
            if raise_error:
                raise AlreadyExistsError()
        except NotFoundError:
            pass
        if not obj:
            obj = cls()
            obj.id = id_str
            obj.meta.id = id_str
            created = True
        if save:
            obj.save()
        return created, obj

    @classmethod
    def get_match_qs(cls, q):
        return {'multi_match':{'query': q, 'fields':cls.MATCH_FIELDS}}


class PostES(BaseESMixin, DocType):
    MATCH_FIELDS = ['name', 'domain']

    title = String()
    body = String()
    created_date = Date()
    updated_date = Date()
    author = String()
    categories = String()
    tags = String()

    class Meta:
        index = 'blog-search'
        doc_type = 'post'

    @classmethod
    def index_post(cls, obj):
        if not isinstance(obj, Post):
            raise TypeError
        created, post_es = cls.get_or_create(id=obj.pk)
        post_es.title = obj.title
        post_es.body = obj.body
        post_es.created_date = obj.created_date
        post_es.updated_date = obj.updated_date
        post_es.author = obj.author.name
        post_es.categories = [cat.name for cat in obj.categories.all()]
        post_es.tags = [tag.name for tag in obj.tags.all()]

        post_es.save()
        return post_es

    @classmethod
    def remove_index(cls, post_id):
        try:
            post_es = cls.get(id=post_id)
        except NotFoundError:
            return None
        post_es.delete()
        return True
