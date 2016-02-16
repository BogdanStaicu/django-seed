import simplejson as json
import requests
import logging

from elasticsearch_dsl import Search, Q, F
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin, DetailSerializerMixin
from rest_framework.exceptions import ParseError

from advisordeck.activity.activity_serializer import _organization
from advisordeck.organization.models import Organization
from advisordeck.search.api.serializers import SearchEntrySerializer
from advisordeck.search.models import ContactES, ContentES, OrganizationES, ContactListES, SearchEntry
from advisordeck.search.tasks import save_search_string
from advisordeck.utils.api.permissions import IsObjectOwner
from advisordeck.utils.api.pagination import PageNumberPaginationES
from advisordeck.content.utils import UserOrganizationData

logger = logging.getLogger('elasticsearch')

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


class QuickSearchView(BaseSearchMixin, APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        q = request.GET.get('q')
        if not q:
            return Response({'errors':['No query param']}, 400)
        broker_dealer = F('term', type=Organization.TYPES.broker_dealer)
        is_inactive = F('term', is_active=False)

        contacts = ContactES.search().query('match', user_permissions=self.request.user.pk).query(ContactES.get_match_qs(q)).execute()
        organization = OrganizationES.search().filter(
            'bool', must_not=[broker_dealer, is_inactive]).query(OrganizationES.get_match_qs(q)).execute()
        lists = ContactListES.search().query('match', user=self.request.user.pk).query(ContactListES.get_match_qs(q)).execute()
        response = {
            'contacts': {
                'count': contacts.hits.total,
                'objects': self.serialize_response_objects(contacts, del_items=['user_permissions'])
            },
            'lists': {
                'count': lists.hits.total,
                'objects': self.serialize_response_objects(lists, del_items=['user'])
            },
            'organizations': {
                'count': organization.hits.total,
                'objects': self.serialize_response_objects(organization)
            }
        }

        return Response(response)


class OrganizationSearchView(BaseSearchMixin, APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        q = request.GET.get('q')
        if not q:
            return Response({'errors':['No query param']}, 400)

        # org_ids = self.request.user.relations.filter(status=Relationship.STATES.active).value_list(['organization_id'])
        # contacts = ContactES.search().query('match', user_permissions=self.request.user.pk).query(ContactES.get_match_qs(q)).execute()
        broker_dealer = F('term', type=Organization.TYPES.broker_dealer)
        is_inactive = F('term', is_active=False)
        organization = OrganizationES.search().filter(
            'bool', must_not=[broker_dealer, is_inactive]).query(OrganizationES.get_match_qs(q)).execute()
        # lists = ContactListES.search().query('match', user=self.request.user.pk).query(ContactListES.get_match_qs(q)).execute()
        response = {
            # 'contacts': {
            #     'count': contacts.hits.total,
            #     'objects': self.serialize_response_objects(contacts, del_items=['user_permissions'])
            # },
            # 'lists': {
            #     'count': lists.hits.total,
            #     'objects': self.serialize_response_objects(lists, del_items=['user'])
            # },
            'count': organization.hits.total,
            'results': self.serialize_response_objects(organization, del_items=['admins', 'members', 'subscribers'])
        }

        if response['count']:
            save_search_string.delay(search_string=q, user_id=self.request.user.pk)

        # user_permissions
        # result = Search(index='gainfully-search', doc_type=['contact','content','organization'])\
        #     .query(ContactES.get_match_qs(q) | ContentES.get_match_qs(q) | OrganizationES.get_match_qs(q))\
        #     .execute()
        # sq = Search(index='gainfully-search', doc_type=['contact','content','organization'])\
        #     .query('match', users=68)\
        #     .query('match', display_name='cristin')
        return Response(response)


class ContentSearchView(BaseSearchMixin, APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        q = request.GET.get('q')
        ids = request.GET.get('ids')
        f = request.GET.get('filter')

        userdata = UserOrganizationData(request.user)
        permission_qs = ContentES.get_permission_filter(userdata)

        search = ContentES.search().filter(permission_qs)

        if ids:
            try:
                ids = [int(id) for id in ids.split(',')]
                search = search.filter('ids', values=ids)
            except ValueError:
                ids = None

        if q:
            search = search.query(ContentES.get_match_qs(q))

        if not ids or f:
            f = ContentES.get_search_filter_args(f)
            filter_qs = ContentES.get_filter_qs(f, userdata)

            if f['sortFilter']['new']:
                if filter_qs:
                    search = search.filter(filter_qs)
                search = search.sort('-created_at')
            else:
                sorting='base'
                if f['sortFilter']['top']:
                    sorting='top'
                if f['sortFilter']['popular']:
                    sorting='popular'

                boost_query = ContentES.get_shareable_boost(userdata, filter_qs, sorting=sorting)
                logger.debug("Boost:{} by user: {}".format(boost_query, userdata.user.id))
                search = search.query(boost_query)


        paginator = PageNumberPaginationES()
        object_list = paginator.paginate_queryset(search, request)

        content_objects = self.process_results(userdata, object_list, del_items=['user_permissions', 'organization_permissions', 'organization_approvals', 'content_lists'])

        if paginator.page.paginator.count:
            save_search_string.delay(search_string=q, user_id=self.request.user.pk)

        content_response = paginator.get_paginated_response(content_objects)
        return content_response

    @classmethod
    def process_results(cls, userdata, items, del_items=None ):
        response = []
        item_data = []
        org_ids = set()

        for item in items:
            # collect data for get_card_permissions
            item_data.append([int(item.id), item.organization_id, bool(item.finra_letter), item.finra_exempt, item.fp_only, item.is_shareable])
            # collect data for organization details
            org_ids.add(item['organization_id'])

            resp_item = item.to_dict()
            if del_items and isinstance(del_items, list):
                for ditem in del_items:
                    if ditem in resp_item:
                        del resp_item[ditem]

            resp_item['id'] = item.meta['id']
            resp_item['_score'] = item.meta['score']
            resp_item['_type'] = item.meta['doc_type']
            response.append(resp_item)

        card_status = userdata.process_cards(item_data)
        org_details = {}
        orgs = Organization.objects.filter(pk__in=org_ids)

        for org in orgs:
            org_details[org.pk] = _organization(org)

        for item in response:
            item.update(card_status[int(item['id'])])
            item['owning_organization'] = org_details[item['organization_id']]

        return response


class SearchEntryViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = SearchEntrySerializer
    permission_classes = (IsAuthenticated, IsObjectOwner,)

    def get_queryset(self):
        return SearchEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        print 'create'
        serializer.save(user = self.request.user)

    def perform_update(self, serializer):
        print '>>>>'
        self.perform_create(serializer)

class BuzzSumoView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, url):

        full_url = 'http://api.buzzsumo.com/search/{}'.format(url)

        query =  dict(request.QUERY_PARAMS.iterlists())
        query.update({'api_key': settings.BUZZSUMO_API_KEY})

        r = requests.get(full_url, params=query)
        content = r.content
        if 'application/json' in r.headers['content-type']:
            content = json.loads(content)

        for header in ['connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade', 'content-encoding']:
            r.headers.pop(header, None)

        return Response(content, r.status_code, headers=r.headers)
