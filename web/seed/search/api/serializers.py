from rest_framework import serializers
from advisordeck.search.models import SearchEntry


class SearchEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchEntry
        fields = ['created_at', 'search_string', 'id']
        read_only_fields = ['created_at', ]