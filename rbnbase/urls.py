from django.contrib import admin
from django.urls import path

from rbnapi import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bnapi/', views.GetBirdName.as_view()),
    path('', views.start_page, name='index'),
]
