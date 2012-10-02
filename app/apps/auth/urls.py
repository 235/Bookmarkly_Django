from django.conf.urls.defaults import patterns, url
from views import register, update, user_login, user_logout

urlpatterns = patterns('',
    url(r'^register$', register, name='register'),
    url(r'^user$', update, name='update'),
    url(r'^login$', user_login, name='login'),
    url(r'^logout$', user_logout, name='logout'),
)
