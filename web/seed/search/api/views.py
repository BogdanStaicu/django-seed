from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin

from seed.search.models import PostES


class BaseSearchMixin(object):

    def serialize_response_objects(self, items, del_items=None):
        response = []
        for item in items:
            resp_item = item.to_dict()
            if del_items and isinstance(del_items, list):
                for ditem in del_items:
                    if ditem in resp_item:
                        del resp_item[ditem]

            resp_item['id'] = item.meta['id']
            resp_item['_score'] = item.meta['score']
            resp_item['_type'] = item.meta['doc_type']
            response.append(resp_item)
        return response


class PostSearchView(BaseSearchMixin, APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        q = request.GET.get('q')
        search = PostES.search()
        if q:
            search = search.query(PostES.get_match_qs(q))
        posts = search.execute()

        response = {
            'posts': {
                'count': posts.hits.total,
                'objects': self.serialize_response_objects(posts)
            },
        }

        return Response(response)
