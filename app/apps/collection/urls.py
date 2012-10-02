from django.conf.urls.defaults import patterns, url
from views import collect_item, collect_items, collect_tags, autocomplete

urlpatterns = patterns('',
    url(r'^bookmark$', collect_items, name='collect_items'),
    url(r'^bookmark/(?P<id>\d+)$', collect_item, name='collect_item'),

    url(r'^tag$', collect_tags, name='collect_tags'),
    url(r'^autocomplete$', autocomplete, name='autocomplete'),
    #TBD:	/json/import
)
