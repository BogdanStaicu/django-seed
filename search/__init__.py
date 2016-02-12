from django.conf import settings
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=settings.ELASTICSEARCH_HOSTS,
                              sniff_on_start=True,
                              sniff_on_connection_fail=True,
                              sniffer_timeout=60)