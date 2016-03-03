import os

ELASTICSEARCH_HOSTS = [
    'http://{}:9200/'.format(os.environ.get('ELASTICSEARCH_PORT_9200_TCP_ADDR', '0.0.0.0')),
]

ES_INDICES_SETTINGS = {
    "settings": {
        "analysis": {
            "filter": {
                "autocomplete_filter": {
                    "type":     "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 20
                }
            },
            "analyzer": {
                "autocomplete": {
                    "type":      "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "autocomplete_filter"
                    ]
                }
            }
        }
    }
}