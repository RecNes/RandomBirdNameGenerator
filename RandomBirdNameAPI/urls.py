from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from rbnapi import api

router = routers.DefaultRouter()
router.register(r'users', api.UserViewSet)
router.register(r'groups', api.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Examples:
    # url(r'^$', 'RandomBirdNameAPI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^bird_name_requested/$', 'rbnapi.views.bird_name_requested', name='bird_name_requested'),
    url(r'^$', 'rbnapi.views.start_page', name='index'),  # HTML Anasayfa

    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
