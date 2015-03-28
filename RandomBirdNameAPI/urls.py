from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RandomBirdNameAPI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^bird_name_requested/$', 'rbnapi.views.bird_name_requested', name='bird_name_requested'),
    url(r'^$', 'rbnapi.views.start_page', name='index'),  # HTML Anasayfa

)

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
