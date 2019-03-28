from django.contrib import admin
from django.urls import path

from rbnapi import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Examples:
    # path('', 'rbnbase.views.home', name='home'),
    # path('blog/', include('blog.paths')),

    path('admin/', admin.site.urls),

    path('bnapi/', views.GetBirdName.as_view()),
    # path('bird_name_requested', views.bird_name_requested, name='bird_name_requested'),
    path('', views.start_page, name='index'),  # HTML Index page
]
