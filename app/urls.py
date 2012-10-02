#from django.conf.urls.static import static
from django.conf.urls.defaults import patterns, url, include

from django.conf import settings
from django.contrib import admin
admin.autodiscover()

scripts = [
    'jquery.min',
    'json2',
    'underscore-min',
    'handlebars.min',
    'backbone-min',
    'jquery.masonry.min',
    'jquery.tagsinput.min',
    'bootstrap-modal',
    'jquery-ui.min',
    'models/Bookmark',
    'models/BookmarksCollection',
    'models/Tag',
    'models/TagsCollection',
    'views/PublicView',
    'views/AccountView',
    'views/EditView',
    'views/BookmarkView',
    'views/BookmarksView',
    'views/TagView',
    'views/TagsView',
    'views/AppView',
    'routers/BookmarklyRouter',
    'App']

templates = ['account', 'bookmark', 'edit', 'footer', 'header', 'index', 'pub', 'tag', 'bookmarks']


handler404 = 'app.apps.views_index.index'
urlpatterns = patterns('',
    (r'^$', 'app.apps.views_index.index'),
    (r'^js/bundle.js$', 'app.apps.views_index.bundle',
        {'scripts': scripts, 'path': settings.STATIC_ROOT + '/js/'}),
    (r'^js/templates.js$', 'app.apps.views_index.templates',
        {'templates': templates, 'path': settings.STATIC_ROOT + '/templates/'}),


    (r'^json/', include('app.apps.auth.urls')),
    (r'^json/', include('app.apps.collection.urls')),


    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)


#if settings.DEBUG and settings.STATIC_ROOT:
if settings.STATIC_ROOT:
    urlpatterns += patterns('',
        url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT + '/css/',
        }),
        url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT + '/js/',
        }),
        url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT + '/images/',
        }),
        url(r'^templates/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT + '/templates/',
        }),
   )
   #static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
