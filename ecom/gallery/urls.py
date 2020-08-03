from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='gallery'
urlpatterns=[
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
]