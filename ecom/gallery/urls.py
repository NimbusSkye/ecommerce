from django.urls import path
from . import views

app_name='gallery'
urlpatterns=[
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('<int:id>', views.detail, name='detail'),
]