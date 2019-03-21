from django.contrib import admin
from django.urls import path

from rbnapi.views import (bird_name_requested, start_page)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Examples:
    # path('', 'RandomBirdNameAPI.views.home', name='home'),
    # path('blog/', include('blog.paths')),

    path('admin/', admin.site.urls),

    path('bird_name_requested/', bird_name_requested, name='bird_name_requested'),
    path('', start_page, name='index'),  # HTML Index page
]
