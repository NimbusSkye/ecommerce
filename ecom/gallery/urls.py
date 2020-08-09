from django.urls import path
from . import views

app_name='gallery'
urlpatterns=[
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('<int:id>/', views.detail, name='detail'),
    path('create/', views.create_cart, name='create_cart'),
    path('<int:id>/add/', views.add_to_cart, name='add_to_cart'),
]