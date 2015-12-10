from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import url, include
from rbnapi.views import (bird_name_requested, start_page)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Examples:
    # url(r'^$', 'RandomBirdNameAPI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^bird_name_requested/$', bird_name_requested, name='bird_name_requested'),
    url(r'^$', start_page, name='index'),  # HTML Anasayfa

    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.

]
