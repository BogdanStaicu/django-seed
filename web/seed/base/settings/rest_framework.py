REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # TODO: set this only when DEBUG is True
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     allow unrestricted access only for platform superusers
    # 'advisordeck.utils.api.permissions.IsSuperUser',
    # ),
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '100/minute',
    #     'user': '600/minute',
    # },
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    # enable and customize pagination
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # and enable clients to override the default page size
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
    # global name for hyperlinked serializers' URL field
    'URL_FIELD_NAME': 'resource_uri',
    # testing defaults
    # 'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    # TODO: perform hand-crafted exception handling
    #EXCEPTION_HANDLER = 'advisordeck.utils.api.views.exception_handler',
    'SEARCH_PARAM': 'q',
}